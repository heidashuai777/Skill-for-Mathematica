(* ::Title:: *)
(*Harmonic-oscillator ground state*)

(* Original deterministic example of the retained style, not a runtime log.
   While developing a new calculation, evaluate and inspect each section
   before writing an output-dependent next step. No disk checkpoint is needed. *)

(* ::Section:: *)
(*Conventions*)

ClearAll[x, m, omega, hbar, assumptions, psi, rho, norm,
  normCheck, x2, hPsi, energy, energyCheck];
assumptions = m > 0 && omega > 0 && hbar > 0;

(* ::Section:: *)
(*Wavefunction*)

psi[x_] := (m omega/(Pi hbar))^(1/4) Exp[-m omega x^2/(2 hbar)];
rho = FullSimplify[
  Conjugate[psi[x]] psi[x],
  Assumptions -> assumptions && Element[x, Reals]
];

(* ::Section:: *)
(*Normalisation*)

norm = Integrate[rho, {x, -Infinity, Infinity}, Assumptions -> assumptions];
normCheck = FullSimplify[norm == 1, Assumptions -> assumptions];
If[! TrueQ[normCheck], Abort[]];

(* ::Section:: *)
(*Position variance*)

(* The state is even, so the mean position is zero. *)
x2 = Integrate[x^2 rho, {x, -Infinity, Infinity}, Assumptions -> assumptions];

(* ::Section:: *)
(*Energy eigenvalue*)

hPsi = -hbar^2/(2 m) D[psi[x], {x, 2}] + m omega^2 x^2 psi[x]/2;
energy = FullSimplify[hPsi/psi[x], Assumptions -> assumptions];
energyCheck = FullSimplify[energy == hbar omega/2, Assumptions -> assumptions];
If[! TrueQ[energyCheck], Abort[]];

{norm, x2, energy}
