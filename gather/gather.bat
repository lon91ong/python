::[Bat To Exe Converter]
::
::fBE1pAF6MU+EWHzeyHU/OhBnRAuSAFujEr0T5tT87v6Pp18hU+MrcIrJlKSXQA==
::YAwzoRdxOk+EWAjk
::fBw5plQjdCqDJG6L5kkDIBREcDSbKGO1CIkb6fzz6vi7pUwJXOctNobY1dQ=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSTk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSTk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpSI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCuDJF6F4Eo1OlVRVAHi
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
set PATH=D:\Anaconda3;D:\Anaconda3\Library\mingw-w64\bin;D:\Anaconda3\Library\usr\bin;D:\Anaconda3\Library\bin;D:\Anaconda3\Scripts;D:\Anaconda3\bin;D:\Anaconda3\condabin;D:\Anaconda3\condabin\Library\mingw-w64\bin;D:\Anaconda3\condabin\Library\usr\bin;D:\Anaconda3\condabin\Library\bin;D:\Anaconda3\condabin\Scripts;D:\Anaconda3\condabin\bin;%PATH%
attrib +H gather.py
python gather.py %~f1
