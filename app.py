from google.cloud import monitoring_v3
import time
import boto100

# Set up your GCP project details
PROJECT_ID = "your-gcp-project-id"
METRIC_TYPE = "custom.googleapis.com/instance/cpu_utilization"

def create_custom_metric():
    """Creates a custom metric in Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{PROJECT_ID}"

    descriptor = monitoring_v3.MetricDescriptor(
        name=project_name,
        type_=METRIC_TYPE,
        metric_kind=monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
        value_type=monitoring_v3.MetricDescriptor.ValueType.DOUBLE,
        description="Custom CPU utilization metric",
    )

    descriptor = client.create_metric_descriptor(name=project_name, metric_descriptor=descriptor)
    print(f"Created custom metric: {descriptor.name}")

def write_time_series():
    """Writes CPU utilization data to Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{PROJECT_ID}"

    # Get current CPU utilization
    cpu_utilization = psutil.cpu_percent(interval=1) / 100.0

    series = monitoring_v3.TimeSeries()
    series.metric.type = METRIC_TYPE
    series.resource.type = "gce_instance"
    series.resource.labels["instance_id"] = "your-instance-id"
    series.resource.labels["zone"] = "your-instance-zone"

    point = monitoring_v3.Point()
    point.value.double_value = cpu_utilization
    now = time.time()
    point.interval.end_time.seconds = int(now)
    series.points.append(point)

    client.create_time_series(name=project_name, time_series=[series])
    print(f"Sent CPU Utilization metric: {cpu_utilization}")

# Create metric descriptor (only needs to run once)
# create_custom_metric()

# Send data every 60 seconds
while True:
    write_time_series()
    time.sleep(60)

