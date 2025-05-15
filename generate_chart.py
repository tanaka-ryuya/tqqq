import tqqq
import tqqq_graph
import tqqq_log_graph


def generate_tqqq_chart():
    tqqq.download_tqqq_data()
    tqqq.download_usd_jpy_rate()
    tqqq_graph.generate_tqqq_linear_chart()

def generate_tqqq_chart_log():
    tqqq.download_tqqq_data()
    tqqq.download_usd_jpy_rate()
    tqqq_log_graph.generate_tqqq_chart()
    
if __name__ == '__main__':
    generate_tqqq_chart()
