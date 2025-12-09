from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

def child_exit(server, worker):
    """
    Gunicorn hook to notify Prometheus exporter of worker exit
    """
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
