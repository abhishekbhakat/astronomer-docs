from airflow.decorators import dag
from pendulum import datetime

# changed operator import statements:
from fivetran_provider_async.operators import FivetranOperatorAsync
from astronomer.providers.core.sensors.filesystem import FileSensorAsync


FIVETRAN_CONNECTOR_ID = "your connector id"


@dag(start_date=datetime(2023, 1, 1), schedule="@daily", catchup=False)
def my_fivetran_dag():
    wait_for_file = FileSensorAsync(  # changed operator name
        task_id="wait_for_file",
        fs_conn_id="in_docker_file_conn",
        filepath="include/{{ ds }}*.csv",
    )

    kick_off_fivetran_sync = FivetranOperatorAsync(  # changed operator name
        task_id="kick_off_fivetran_sync",
        fivetran_conn_id="fivetran_conn",
        connector_id=FIVETRAN_CONNECTOR_ID,
    )

    wait_for_file >> kick_off_fivetran_sync


my_fivetran_dag()
