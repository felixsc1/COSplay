---
title: 'COSplay: Contrast Optimized Stimulation Player'
tags:
- bids
- optogenetics
- electrophysiology
- sensory-stimulation
- trigger-events
- fMRI
- stimulus-evoked
- Bruker
- ParaVision
- contrast-optimized-stimulation
- lab-equipment
- TTL
- BNC
authors:
- name: Florian Aymanns
  affiliation: 1
- name: Markus Rudin
  affiliation: 2
- name: Horea-Ioan Ioanas
  orcid: 0000-0001-7037-2449
  affiliation: 2
affiliations:
- name: Department of Information Technology and Electrical Engineering, ETH Zurich
  index: 1
- name: Institute for Biomedical Engineering, ETH and University of Zurich
  index: 2
date: 20 February 2018
bibliography: paper.bib
---

# Summary

In many research areas, the functioning of complex systems is probed by measuring stimulus-evoked responses.
Commonly, stimulus train delivery is coordinated by in-house and/or proprietary solutions, which are often ill-documented, expensive, poorly reproducible, high-maintenance, and unsustainable.
Here we present a fully Free and Open Source (FOSS) and hackable framework consisting of a Micro/Python package and a simple compatible circuit schema (see below),
which can be used to build and operate a stimulus train delivery device with up to microsecond accuracy.

![Circuit schema.](documentation/circuit.png)

The software supports highly diverse types of stimulus trains - which can be specified in a format that accommodates most experimental scenarios, including:

* amplitude modulation (up to 3.3V)
* event-related designs
* block designs
* tonic stimulation
* multiple stimulation channels
* short-circuit output

The package was extensively tested for viability in a functional magnetic resonance imaging (fMRI) setting, and is used in ongoing investigations using optogenetic and electrical stimulation [@drlfom] [@fatihm] [@felix].
The flexible stimulus train specification is BIDS-conform [@BIDS], and can automatically be parsed for analysis by modern neuroimaging software, including SAMRI [@SAMRI].

Additionally, the software seamlessly interfaces with the Bruker ParaVision (TM) directory structure, and is able to reposit stimulus summaries in corresponding data paths.
This makes COSplay excellently suited for automating the workflow and increasing the reproducibility of small animal MRI studies - while not compromising its potential for other scenarios.

# References
