# Gears Average Field

This demonstrates using Redis Gears to average fields as the data is collected.

## Goals

* Only keep running averages in Redis
* Minimize bulk loading and batch processing
* Send data to Redis as it is ready
* Use Redis as the compute and serving engine

## Description

A backend system is running cash flow scenarios projected across a number of
years. Each year contributes to the average for the scenario and there can be
1000s of scenarios. The `create_cashflow.py` script simulates creating this data
and adds it as a Redis Hash identified as `cash_flow:S:Y` where S is the
scenario and Y is the year in that scenario. A Redis Gears recipe watches for
`cash_flow:[0-9]+:[0-9]+`, updates `cash_flow_average:S`, and adds the
`cash_flow*` key to `consumed_keys`, a Redis List indicating it can be deleted.
A Redis Stream, `run_log` is used to capture log messages.

### Calculating a Running Average

Yes, I had to [look this up](https://math.stackexchange.com/questions/22348/how-to-add-and-subtract-values-from-an-average).

$s=\frac{a_1+...+a_n}{n}$

$s'=\frac{a_1+...+a_n+a_{n+1}}{n+1}=\frac{(n*s)+a_{n+1}}{n+1} = \frac{(n+1)s+a_{n+1}}{n+1} - \frac{s}{n+1} = s + \frac{a_{n+1}-s}{n+1}$

## Requirements

My apologies as I have not Dockerized the data generator yet.

* Python 3
* Poetry (or whatever venv manager you prefer. Or not)
* Redis

## v.Next

* Async/co-routines
* Dockerize
* Time Series and visualiztion
