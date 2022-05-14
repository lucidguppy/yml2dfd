#!/usr/bin/env python
# Copyright 2022 Matthew Karas
from copy import copy

import click
import yaml
from graphviz import Digraph
from yaml import Loader


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--output-format", type=click.STRING, default="png")
def main(input, output, output_format):
    with open(input, "r") as fid:
        data = fid.read()
        data_flow_spec = build_diagram(data)
        data_flow_spec.render(output, view=True, format=output_format)


def build_diagram(data):
    data_flow_spec = yaml.load(data, Loader=Loader)
    diagram = Digraph(name=data_flow_spec["title"], comment=data_flow_spec["title"])
    diagram.attr(rankdir="LR")
    nodes = set(data_flow_spec["process_names"])
    data_flows = set(data_flow_spec["data_flows"])
    untouched_nodes = copy(nodes)
    for receiver in data_flow_spec['receivers']:
        diagram.node(receiver, shape="box")
    for originator_name, originator in data_flow_spec['originators'].items():
        diagram.node(originator_name, shape="box")
        if "outputs" in originator:
            for output, output_dict in originator["outputs"].items():
                if output_dict is None:
                    if output not in data_flows:
                        raise RuntimeError(f"{output=} was not defined as a data flow")
                    data_flows.remove(output)
                    diagram.node(output, shape="plain")
                    diagram.edge(originator_name, output)
                elif "to" in output_dict:
                    if output not in data_flows:
                        raise RuntimeError(f"{output=} was not defined as a data flow")
                    data_flows.remove(output)
                    diagram.edge(originator_name, output_dict["to"], label=output)
                else:
                    raise RuntimeError("Parse error")

    for process, process_config in data_flow_spec["processes"].items():
        if process not in nodes:
            raise RuntimeError(f"Encountered {process=} not enumerated in process names")
        else:
            untouched_nodes.remove(process)
        diagram.node(process, shape="circle")
        if "inputs" in process_config:
            for input in process_config["inputs"]:
                if input not in data_flows:
                    raise RuntimeError(f"{input=} was not defined as a data flow")
                data_flows.remove(input)

                diagram.node(input, shape="plain")
                diagram.edge(input, process)
        if "sources" in process_config:
            for source in process_config["sources"]:
                if source not in data_flows:
                    raise RuntimeError(f"{source=} was not defined as a data flow")
                data_flows.remove(source)
                diagram.node(source, shape="underline")
                diagram.edge(source, process)
        if "outputs" in process_config:
            for output, output_dict in process_config["outputs"].items():
                if output_dict is None:
                    if output not in data_flows:
                        raise RuntimeError(f"{output=} was not defined as a data flow")
                    data_flows.remove(output)
                    diagram.node(output, shape="plain")
                    diagram.edge(process, output)
                elif "to" in output_dict:
                    if output not in data_flows:
                        raise RuntimeError(f"{output=} was not defined as a data flow")
                    data_flows.remove(output)
                    diagram.edge(process, output_dict["to"], label=output)
                else:
                    raise RuntimeError("Parse error")
        if "sinks" in process_config:
            for sink in process_config["sinks"]:
                if sink not in data_flows:
                    raise RuntimeError(f"{output=} was not defined as a data flow")
                data_flows.remove(sink)
                diagram.node(sink, shape="underline")
                diagram.edge(process, sink)

    if untouched_nodes:
        raise RuntimeError(f"{untouched_nodes=} need definition")
    if data_flows:
        raise RuntimeError(f"{data_flows=} weren't used")
    return diagram


if __name__ == "__main__":
    main()
