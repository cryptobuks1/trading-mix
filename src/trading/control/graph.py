from trading.events import bind


def pause_graph_on(pauseEvent, pause_graph):
    bind(pauseEvent, lambda peak_analysis: pause_graph())
