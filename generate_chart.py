def generate_tqqq_chart():
    import tqqq
    import tqqq_graph
    tqqq.download_tqqq_data()
    tqqq.download_usd_jpy_rate()
    tqqq_graph.generate_tqqq_linear_chart()

def generate_tqqq_chart_log():
    import tqqq
    import tqqq_log_graph
    tqqq.download_tqqq_data()
    tqqq.download_usd_jpy_rate()
    tqqq_log_graph.generate_tqqq_chart()
    
if __name__ == '__main__':
    generate_tqqq_chart()
    generate_tqqq_chart_log()
