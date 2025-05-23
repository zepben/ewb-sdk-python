---
id: sdk-overview
title: Overview
slug: /
---

# EWB SDK

The EWB SDK contains everything necessary to write software for the EWB platform. Common use cases are:
- Writing ingestors to process source data into the EWB CIM data model
- Pulling network data from a EWB server for analysis

The following features are present in the Python version of the EWB SDK:

| Feature name                     | Description                                                                                           |
|----------------------------------|-------------------------------------------------------------------------------------------------------|
| CIM data model                   | The CIM data model for networks, customers, and diagrams used in EWB.                                 |
| Tracing                          | A set of utility functions that can trace through a network, accounting for connectivity/phasing.     |
| Network consumer                 | The ability to pull network data from EWB into an in-memory CIM data model.                           |
| Customer consumer                | The ability to pull customer data from EWB into an in-memory CIM data model.                          |
| Diagram consumer                 | The ability to pull diagram data from EWB into an in-memory CIM data model.                           |
| CIM database reading/writing     | The ability to save and load an in-memory CIM data model into databases.                              |
