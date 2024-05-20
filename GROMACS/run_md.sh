#!/bin/bash

#--------------- Lysozyme in water --------------------#

. /usr/local/gromacs/bin/GMXRC

#-- Get a topology file, a position retrain file, a post-processed structure file
# spce is the water model
# 15: OPLS-AA/L all-atom force field (2001 aminoacid dihedrals)
echo 15 | gmx pdb2gmx -f 1aki.pdb -o 1aki_processed.gro -water spce

#-- Create the limits of the system
gmx editconf -f 1aki_processed.gro -o 1aki_newbox.gro -d 1.0 -bt cubic

#-- Fill the vaccum with water molecules
gmx solvate -cp 1aki_newbox.gro -cs spc216.gro -o 1aki_solv.gro -p topol.top

#-- Add ions to the system
gmx grompp -f ions.mdp -c 1aki_solv.gro -p topol.top -o ions.tpr
echo 13 | gmx genion -s ions.tpr -o 1aki_solv_ions.gro -p topol.top -pname NA -nname CL -nn 8

#-- Relax the system (energy minimization)
gmx grompp -f minim.mdp -c 1aki_solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em

#-- NVT simulation : constant Number of particles, Volume, and Temperature. Stabilize the temperature of the system
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -v -deffnm nvt

#-- NPT simulation: Number of particles, Pressure, and Temperature are all constant. Stabilize the pressure
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt

#-- The system is now well-equilibrated at the desired temperature and pressure. Release the position restraints and run production MD for data collection
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_1.tpr
gmx mdrun -v -deffnm md_0_1
