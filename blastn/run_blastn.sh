#!/bin/bash

makeblastdb -in chr6.fna -dbtype nucl -parse_seqids -out chr6
blastn -db chr6 -query hla-b.fsa -out results.out
