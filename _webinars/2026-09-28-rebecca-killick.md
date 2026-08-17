---
title: "How should we be performing time series simulation studies?"
speaker: "Rebecca Killick"
affiliation: "Associate Director of Research, School of Mathematical and Statistical Sciences, Clemson University"
date: 2026-09-28
time: "12:00 PM - 1:30 PM ET"
speaker_url: "https://www.lancs.ac.uk/~killick/"
speaker_image: "/assets/images/speakers/rebecca-killick.jpg"
registration_url: "https://events.teams.microsoft.com/event/372324fe-914c-4d6e-9942-770cfbd474d6@17f1a87e-2a25-4eaa-b9df-9d439034b080"
slides_url: ""
youtube_url: ""
materials_url: ""
materials:
  - title: "Published Paper"
    url: "https://www.tandfonline.com/doi/full/10.1080/00031305.2026.2695128"
---
## Abstract

<!-- archive-abstract-start -->
As a community, we don't do simulation studies well - myself included! We often produce theory for general ARMA orders but give simulation studies with one anecdotal case or maybe a grid of values for an AR or MA order 1 process. Given the wide applicability and use of these models in the wild, we should be demonstrating when methods work well and when they don't in an honest way so practitioners can choose the best methods for the data at hand.

To run robust simulations involving ARMA (Autoregressive Moving Average) generated data rather than picking anecdotal cases, it is preferable to choose parameters representative of the full sample space corresponding to causal and invertible difference equations. Specific parameter values can either be selected via a fixed design experiment or a random effects experiment. Implementation of either of these methods requires quantifying these parameter spaces. These spaces are not described for ARMA orders higher than two in time series texts, nor are they readily available in the literature. This talk describes how to determine the parameter spaces for higher-order processes, with explicit descriptions and graphics of the parameter space up to order 4. To randomly generate parameters in these spaces, methods that generate parameters and use roots of polynomials to check for causality are highly inefficient, while first generating roots of polynomials and then determining parameters is cumbersome and lacks a simple connection to the parameter space. We provide an efficient algorithm to generate parameters within these spaces. Parameters can be generated uniformly across possible correlations or uniformly in the parameter space. Furthermore, a simple measure of total correlation is proposed for autoregressive processes of arbitrary order, which can be used within simulation studies to test statistical methods under "high" and "low" correlation scenarios.
<!-- archive-abstract-end -->

## Speaker Bio

Rebecca Killick received their PhD degree in Statistics from Lancaster University, and was a Professor and Director of Research until 2026. Now they are Associate Director of Research for the School of Mathematical and Statistical Sciences at Clemson University. In 2019 they were the first UK recipient of the "Young Statistician of the Year" award from the European Network for Business and Industrial Statistics which recognizes the work of young people in introducing innovative methods, promoting the use of statistics and/or successfully using it in daily practice. Rebecca sees their research as a feedback loop, being inspired by problems in real world applications, creating novel methodology to solve those problems and then feeding these back into the problem domain. Their primary research interests lie in development of novel methodology for the analysis of univariate and multivariate nonstationary time series models. Rebecca is highly motivated by real world problems and has worked with data in a range of fields including Bioinformatics, Energy, Engineering, Environment, Finance, Health, Linguistics and Official Statistics. Rebecca is passionate about ensuring the availability and accessibility of research in the form of open-source software. They are Editor in Chief of the Journal of Statistical Software and Journal of Computational and Graphical Statistics.
