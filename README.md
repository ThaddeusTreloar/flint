# flint

Flint is designed to provide a framework for fast iteration of machine learning models for financials forecasting.
!! flint is still currently under development !!
Beyond this is aims to provide enough modularity to enable deployment on home devices using chron and webserver modules (Django) so that one can automate their predictive models fit functions.
Classes and interfaces are provided to create modules of different types for various purposes. Want to create a module that takes output from a module and sends it to an API? No problem. Want to create an API that takes socket input and performs actions? Easy.
This readme is subject to change as the project evolves.

## Structure

The system is broken up into several parts to enable modularity.

### Kernel
This is the central hub that connect the different handlers

### Handlers
These prodivde an interface between different module types.

### Input
An object type that interacts with the input handler and provides facilities for user input (console, webserver, chron)

### Output
An object type that interacts with the output handler and provides output functionality (console, sql, plaintext, binary)

### Source
An object type that interacts with the source handler and provides all other modules with remote data (alphavantage, yahoofinance, etc...)

### Preprocessing
These are modules that perform transformations on raw data for use by an ML/AI model. The syntax for this is under development.

### MLNN
Various machine learning and neural net models for data fitting. Currently planned modules are sklearn.SVR, sklearn.SVM, and tensorflowlite (with coral chip support).

## Licensing
All software is licensed under GPLv3, a copy of which can be found in this repository or at [GNU.org](https://www.gnu.org/licenses/gpl-3.0.en.html)

