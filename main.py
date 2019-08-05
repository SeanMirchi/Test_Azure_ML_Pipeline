from azureml.core import Workspace, RunConfiguration, Experiment, Run
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline, PipelineData, PipelineParameter
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.conda_dependencies import CondaDependencies
import secret

def authenticate():
    print(f'TENANT_ID : {secret.TENANT_ID}')
    svc_pr = ServicePrincipalAuthentication(
        tenant_id=secret.TENANT_ID,
        service_principal_id=secret.SERVICE_PRINCIPAL_APP_ID,
        service_principal_password=secret.SERVICE_PRINCIPAL_SECRET
    )
    return svc_pr
    

def create_pipeline():
    ws = Workspace.from_config(auth=authenticate())
    def_data_store = ws.get_default_datastore()
    run = Run.get_context()

    project_folder = "project"

    read_output = PipelineData(
        "read_output",
        datastore=def_data_store,
        output_name="read_output"
        )
    process_out = PipelineData(
        "process_out",
        datastore=def_data_store,
        output_name="process_out"
        )

    # hist, line, scatter 
    chart_type = PipelineParameter(name="chart_type", default_value="line")

    # Check if compute exist
    compute_name = "Dedicated-DS3-v2"
    vm_size = "STANDARD_D3_V2"
    if compute_name in ws.compute_targets:
        compute_target = ws.compute_targets[compute_name]
        if compute_target and type(compute_target) is AmlCompute:
            print('Found compute target: ' + compute_name)
    else:
        # create the compute target
        print('Creating a new compute target...')
        provisioning_config = AmlCompute.provisioning_configuration(vm_size=vm_size, min_nodes=0, max_nodes=4)
        compute_target = ComputeTarget.create(ws, compute_name, provisioning_config)
        compute_target.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)

    # create run config for our python steps
    def conda_deps():
        deps = CondaDependencies(f'{project_folder}/environment.yml')
        deps.add_channel("conda-forge")
        deps.add_conda_package('curl')
        return deps
    run_config = RunConfiguration(conda_dependencies=conda_deps())
    run_config.environment.docker.enabled = True
    run_config.environment.spark.precache_packages = False

     # Create each step for our pipeline
    read_data = PythonScriptStep(
        name="read_data",
        script_name="read_data.py",
        arguments=["read-data", 
                   "--output-path", read_output],
        outputs=[read_output],
        compute_target=compute_target,
        source_directory=project_folder,
        runconfig=run_config
        )
    
    pre_process = PythonScriptStep(
        name="pre_process",
        script_name="pre_process.py",
        arguments=["pre-process",
                   "--input-path", read_output, 
                   "--output-path", process_out],
        inputs=[read_output],
        outputs=[process_out],
        compute_target=compute_target,
        source_directory=project_folder,
        runconfig=run_config
        )
    
    visualize = PythonScriptStep(
        name="visualize",
        script_name="visualize.py",
        arguments=["visualize",
                   "--input-path", process_out, 
                   "--chart", chart_type],
        inputs=[process_out],
        compute_target=compute_target,
        source_directory=project_folder,
        runconfig=run_config
        )

    # list of steps to run
    steps = [read_data, pre_process, visualize]

    # Build the pipeline
    test_pipeline = Pipeline(workspace=ws, steps=[steps])

    # Submit the pipeline to be run - In the same experiment
    pipeline_run = run.experiment.submit(test_pipeline)
    pipeline_run.wait_for_completion()

    # Publish the pipeline to make it available in ML-Service -> Pipelines
    # test_pipeline.publish(name="Test_Pipeline", description="Publish the test pipeline", version="0.1")

if __name__ == "__main__":
    create_pipeline()
