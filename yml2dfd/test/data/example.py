# Copyright 2022 Matthew Karas
simple = """
title: Process Invoice
originators:
  customer:
    outputs:
      credited invoice copy:
        to: record payment
receivers:
  - some guy
data_flows:
  - payment
  - credited invoice copy
  - check
  - bank deposit
  - receivables file
  - archive file
  - noc file
  - address db table
  - bank deposit
process_names:
  - credit invoice
  - record payment
  - deposit funds
processes:
  credit invoice:
    sources:
      - noc file
    outputs:
      credited invoice copy:
        to: record payment
      check:
        to: deposit funds
  record payment:
    sources:
      - address db table
    sinks:
      - receivables file
      - archive file
  deposit funds:
    outputs:
      bank deposit:
        to: some guy
"""
