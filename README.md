Btor2-Select is an algorithm selector for hardware modeling checking problems in the Btor2 format.

## Component Verifiers
Here, a verifier refers to the implementation of a specific verification algorithm within a particular tool. Our algorithm portfolio includes a total of 21 component verifiers. In addition to hardware verifiers, our selector also supports the selection of software verifiers for Btor2 instances by first translating them into behaviorally equivalent C programs using [Btor2C](https://gitlab.com/sosy-lab/software/btor2c).

List of our component verifiers (tool: algorithms>):

* [ABC](https://github.com/berkeley-abc/abc): BMC, IMC, PDR, SCORR-BMC, SCORR-IMC, SCORR-PDR
* [AVR](https://github.com/aman-goel/avr): BMC-Boolector, BMC-Yices2, k-induction, PDR
* [BtorMC](https://boolector.github.io/): BMC, k-induction-sp, k-induction
* [CBMC](https://www.cprover.org/cbmc/): BMC, k-induction
* [CPAchecker](https://cpachecker.sosy-lab.org/): IMC
* [ESBMC](https://github.com/esbmc/esbmc): BMC, k-induction
* [KLEE](https://klee-se.org/)
* [Pono](https://github.com/stanford-centaur/pono): BMC, ic3bits, ic3sa, ind, interp

## Algorithm Selection Model
Our algorithm selectors are based on [cost-sensitive pairwise classifiers](http://www.cs.ubc.ca/labs/beta/Projects/SATzilla/SATzilla2012final.pdf), a widely used approach in algorithm selection. During training, a binary classifier is trained for each pair of component verifiers to predict which one would perform better in terms of the PAR-2 score. Each training sample is weighted by the PAR-2 difference between the verifier pair. During inference, for a given instance, all pairwise classifiers are evaluated, and the verifier that receives the highest votes from these classifiers is selected. We use [XGBoost](https://xgboost.readthedocs.io/en/stable/) as the classifier model. 

## Instance Feature
Btor2 instances are represented as Bag of Keywords, which counts the occurrence of each keyword in the file. We have identified a total of 69 keywords, such as *state*,  *not*, and *add*.

## Model Training
We have collected a comprehensive [word-level hardware model-checking benchmark dataset](https://gitlab.com/sosy-lab/research/data/word-level-hwmc-benchmarks/) for model training. In this study, we only focus on the benchmarks without arrays.

The pairwise XGBoost models were trained on a MacBook Air with an M2 chip and 8 GB memory. All executions of the verifier-instance pair were conducted on machines running Ubuntu 22.04 (64 bit), each with a 3.4 GHz CPU (Intel Xeon E3-1230 v5) with 8 processing units and 33 GB of RAM. Each task was limited to 2 CPU cores, 15 min of CPU time, and 15 GB of RAM. We used [BenchExec](https://github.com/sosy-lab/benchexec) to ensure reliable resource measurement and reproducible results. 

## Contributors
* [John Lu](https://johnlyu2.github.io/) 
* [Po-Chun Chien](https://www.sosy-lab.org/people/chien/)
* [Nian-Ze Lee](https://www.sosy-lab.org/people/lee/)
* [Vijay Ganesh](https://vganesh1.github.io/)

## License
Btor2-Select is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). The submodule `btor2kwcount` is largely based on codes from [Btor2Tools](https://github.com/Boolector/btor2tools), which is licensed under the [MIT License](btor2kwcount/LICENSE.txt).