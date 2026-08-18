---
title: "Surprises in time series analysis"
speaker: "Rob J Hyndman"
affiliation: "Vice-Chancellor's Distinguished Professor of Statistics, Department of Econometrics and Business Statistics, Monash University"
date: 2026-10-26
permalink: /webinars/rob-hyndman/
time: "6:00 PM - 7:30 PM ET"
speaker_url: "https://robjhyndman.com/"
speaker_image: "/assets/images/speakers/rob-hyndman.jpg"
registration_url: "https://events.teams.microsoft.com/event/cab77726-7373-4172-9079-7710c45db522@17f1a87e-2a25-4eaa-b9df-9d439034b080?source=copyLinkLegacyShareEventDialog"
slides_url: ""
youtube_url: ""
materials_url: ""
materials:
  - title: "weird R Package"
    url: "https://pkg.robjhyndman.com/weird/"
  - title: "That's Weird: Anomaly Detection Using R"
    url: "https://otexts.com/weird"
  - title: "Anomaly Detection Using Surprisals"
    url: "http://robjhyndman.com/publications/surprisals.html"
---
## Abstract

<!-- archive-abstract-start -->
I will present a statistical framework for identifying anomalies in three time series settings: unusual observations within a single historical series, unusual series within a large collection, and real-time surveillance of incoming data streams.

In each case, anomalies are identified using a probabilistic approach based on "surprisal values" - equal to minus the log (conditional) density of each observation - with extreme value theory used to model the tail of the surprisal distribution and avoid strong parametric assumptions.

The methods will be illustrated using the [{weird}](https://pkg.robjhyndman.com/weird/) package for R, with examples including French and US mortality rates, and pharmaceutical sales.
<!-- archive-abstract-end -->

## Speaker Bio

Rob J Hyndman FAA FASSA holds the position of Vice-Chancellor's Distinguished Professor of Statistics in the [Department of Econometrics and Business Statistics](https://monash.edu/business/ebs) at [Monash University](https://www.monash.edu/), and is an elected Fellow of both the [Australian Academy of Science](https://www.science.org.au/profile/rob-hyndman) and the [Academy of Social Sciences in Australia](https://socialsciences.org.au/academy-fellow/?sId=0032v00003JxrvjAAB). He is the author of over 230 research papers and 6 books in statistical science. In 2007, he received the [Moran medal](https://www.science.org.au/past-winners/2007-awardees#moran) from the Australian Academy of Science for his contributions to statistical research, especially in the area of statistical forecasting. In 2021, he received the [Pitman medal](https://www.statsoc.org.au/Pitman-Medal-Recipients) from the Statistical Society of Australia. For over 40 years, Rob has maintained an active consulting practice, assisting hundreds of companies and organizations around the world. He has won awards for his research, teaching, consulting and graduate supervision.

## Software

The methods will be illustrated using the [`weird`](https://pkg.robjhyndman.com/weird/) package for R.

## References

- Hyndman, Rob J. 2026. *That's Weird: Anomaly Detection Using R*. [https://OTexts.com/weird](https://otexts.com/weird).
- Hyndman, Rob J, and David T Frazier. 2026. "Anomaly Detection Using Surprisals." [http://robjhyndman.com/publications/surprisals.html](http://robjhyndman.com/publications/surprisals.html).
