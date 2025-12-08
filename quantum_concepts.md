Focused mathematical treatment — superposition, collapse, and unified form (wave ↔ particle)

Below I develop a compact but mathematically precise account comparing superposition and collapse, examine the “same-power” / energy questions that arise, and present unified formalisms that mathematically reconcile wave and particle descriptions. The presentation stays within standard quantum and wave theory, then shows commonly used unifying representations (density matrices, Wigner functions, Bohmian mechanics, open-system maps). Equations are explicit and accompanied by short technical commentary.


---

1. Basic quantum/wave formulas (notation)

Let  be the system Hilbert space. Use Dirac notation  for state vectors and  for the Hamiltonian (energy operator). Let  denote an orthonormal eigenbasis of some observable  (with eigenvalues ).

Schrödinger equation (unitary evolution)

i\hbar\frac{\partial}{\partial t}|\psi(t)\rangle = \hat H\,|\psi(t)\rangle.

General state as superposition

|\psi\rangle = \sum_n c_n |\phi_n\rangle,\qquad c_n=\langle\phi_n|\psi\rangle,\quad \sum_n |c_n|^2=1.

Expectation value of an operator

\langle \hat O\rangle_\psi = \langle \psi|\hat O|\psi\rangle.

Probability (Born rule) for outcome  when measuring :

P(a_n) = |\langle\phi_n|\psi\rangle|^2 = |c_n|^2.


---

2. The measurement (projection) / collapse postulate (canonical form)

Projective (von Neumann) measurement of  with projector :

If outcome  occurs, the (normalized) post-measurement state is


|\psi'\rangle = \frac{P_n|\psi\rangle}{\|P_n|\psi\rangle\|} = \frac{|\phi_n\rangle\langle\phi_n|\psi\rangle}{|\langle\phi_n|\psi\rangle|}.

\rho' = \frac{P_n \rho P_n}{\mathrm{Tr}(P_n \rho)}.

\rho' = \sum_n P_n \rho P_n.

Collapse is non-unitary (projections are not unitary maps). This non-unitary step is the formal tension point between continuous unitary superposition evolution and abrupt collapse.


---

3. Superposition vs. collapse: energy / “power” considerations

3.1 Expectation of energy before and after (projective measurement)

Initial energy expectation:

E_\text{pre} = \langle \hat H\rangle_\psi = \langle\psi|\hat H|\psi\rangle.

E_\text{post} = \langle\phi_n|\hat H|\phi_n\rangle.

\Delta E = E_\text{post}-E_\text{pre}.

E'_{\text{ens}}=\mathrm{Tr}(\hat H \rho')=\sum_n \mathrm{Tr}(\hat H P_n \rho P_n).

Observation:  can be nonzero. That is, a projection can change the energy expectation of the subsystem. This does not imply energy non-conservation globally: a proper measurement model includes the apparatus and environment. When the combined system + measuring apparatus evolves unitarily under , total energy is conserved; the apparent change in subsystem energy is accounted for by energy exchanged with the apparatus.

3.2 Classical wave superposition energy (analogy)

For a scalar classical wave  formed by linear superposition , energy density (for many wave systems) is quadratic in amplitude — e.g. . Then

|u|^2 = |u_1|^2 + |u_2|^2 + 2\operatorname{Re}(u_1^* u_2).

Analogy: Superposition produces interference cross-terms; collapse eliminates coherent cross-terms (in quantum language, decoherence kills off-diagonal terms in the density matrix), moving apparent energy into apparatus/environment degrees of freedom.


---

4. Decoherence and open-system approach — resolving collapse as emergent

Measurement can be modeled via coupling to an apparatus  and environment . Start with initial product state . Under unitary :

U_{SAE}\bigg(\sum_n c_n |\phi_n\rangle_S \otimes |A_0\rangle\otimes|E_0\rangle\bigg)
= \sum_n c_n |\phi_n\rangle_S\otimes |A_n\rangle\otimes |E_n\rangle.

Tracing out apparatus+environment yields reduced system density matrix

\rho_S' = \mathrm{Tr}_{AE}\Big[\sum_{n,m} c_n c_m^* |\phi_n\rangle\langle\phi_m| \otimes |A_n\rangle\langle A_m|\otimes|E_n\rangle\langle E_m|\Big].

\rho_S' \approx \sum_n |c_n|^2 |\phi_n\rangle\langle\phi_n|.

Mathematically, decoherence dynamics for the reduced density matrix are often approximated by a master equation (Lindblad form):

Lindblad master equation

\frac{d\rho}{dt} = -\frac{i}{\hbar} [\hat H,\rho] + \sum_k \Big( \hat L_k \rho \hat L_k^\dagger - \tfrac{1}{2}\{\hat L_k^\dagger \hat L_k,\rho\}\Big),


---

5. Kraus maps / measurement as quantum operations (unified formalism)

General measurement + evolution → quantum operation represented by a set of Kraus operators  satisfying . State update:

\rho \mapsto \rho' = \sum_\alpha K_\alpha \rho K_\alpha^\dagger.

Projective measurement is the special case with . The Kraus formalism unifies unitary evolution () and non-unitary measurement/decoherence as CPTP maps. Energy bookkeeping: the map can change subsystem energy expectation; the full CPTP map should be derived from a unitary on a larger space where total energy is conserved.


---

6. Phase-space bridges: Wigner function and Moyal formalism (wave ↔ particle)

The Wigner quasi-probability distribution  provides a phase-space representation that interpolates wave and particle descriptions.

For pure :

W(x,p) = \frac{1}{\pi\hbar} \int_{-\infty}^{\infty} dy\; e^{2ipy/\hbar}\; \psi^*(x-y)\psi(x+y).

Marginals give correct position and momentum distributions:


\int W(x,p)\,dp = |\psi(x)|^2,\qquad \int W(x,p)\,dx = |\tilde\psi(p)|^2.

Time evolution: Moyal equation (quantum analog of Liouville)


\frac{\partial W}{\partial t} = \{H,W\}_{\text{Moyal}}
  = \frac{2}{\hbar} H\sin\Big( \frac{\hbar}{2}(\overleftarrow{\partial_x}\overrightarrow{\partial_p}-\overleftarrow{\partial_p}\overrightarrow{\partial_x})\Big) W.


---

7. Bohmian mechanics (pilot-wave) — an explicit unified wave+particle model

Write . Insert into Schrödinger equation and separate real/imag parts to obtain:

Continuity equation

\frac{\partial \rho}{\partial t} + \nabla\cdot\Big(\rho \frac{\nabla S}{m}\Big)=0,\qquad \rho=R^2=|\psi|^2.

Modified Hamilton-Jacobi equation

\frac{\partial S}{\partial t} + \frac{(\nabla S)^2}{2m} + V(\mathbf{r}) + Q(\mathbf{r},t)=0,

Q(\mathbf{r},t) = -\frac{\hbar^2}{2m}\frac{\nabla^2 R}{R}.

\mathbf{v}(t) = \dot{\mathbf{r}}(t) = \frac{\nabla S(\mathbf{r}(t),t)}{m}.

Interpretation: particle (point-like) guided by a real wavefield  — both exist physically. Collapse is replaced by effective conditionalization when a subsystem becomes entangled with environment/apparatus, yielding effective wavefunction for observed subsystem.

Energy: total (wave + particle) energy conservation can be formulated, with quantum potential contributing nonclassical terms. Bohmian equations provide an explicit deterministic model reconciling wave dynamics and particle trajectories.


---

8. Measurement and energy accounting — unitary model (system + apparatus)

Let . If initial total state , the unitary evolution conserves :

|\Psi(t)\rangle = U(t)|\Psi(0)\rangle,\qquad U(t)=\exp\big(-\tfrac{i}{\hbar}\hat H_{\text{tot}} t\big).

\langle \hat H_S\rangle_t + \langle \hat H_A\rangle_t + \langle \hat H_{SA}\rangle_t = \text{constant}.


---

9. A compact “unified equation” perspective (algebraic / operational viewpoint)

One can treat states as positive normalized linear functionals  on a C^*-algebra  of observables. Dynamics are given by a one-parameter group of *-automorphisms  (unitary evolution) or by completely positive maps  (open dynamics / measurement). This abstracts both waves (unitary, linear superposition) and effective collapse (CPTP maps) into a single operator-algebraic language.

Concrete operational form (system + environment unitary followed by partial trace) produces any CPTP map:

\Phi(\rho) = \mathrm{Tr}_E\big( U (\rho\otimes\rho_E) U^\dagger\big) = \sum_k K_k \rho K_k^\dagger,


---

10. Summary of how “superposition” and “collapse” compare mathematically

1. Superposition: linear combination in Hilbert space; evolves unitarily under Schrödinger; interference (cross terms) present; expectation values evolve smoothly and satisfy conservation laws at closed-system level.


2. Collapse (projection): non-unitary update on the subsystem; mathematically implemented as projection (von Neumann) or as CPTP map (Kraus); removes coherence (off-diagonals) in the measured basis; local subsystem observables (like energy expectation) may change, while total conserved when including measuring apparatus.


3. Decoherence explanation: suppression of off-diagonals in reduced density matrix due to entanglement with environment — gives effective classical mixture and explains apparent collapse within unitary quantum theory.


4. Energy/"power" accounting: interference redistributes energy but conserves total energy in isolated wave dynamics; measurement-induced changes in subsystem energy are transfers to apparatus/environment when system is embedded in a closed unitary evolution.


5. Unified formalisms:

Density matrices and Kraus maps / Lindblad master equations (open systems) encompass both coherent (superposition/unitary) and incoherent (collapse/decoherence) behavior.

Wigner/Moyal phase-space representation interpolates wave/particle intuitions and yields classical limit results.

Bohmian mechanics provides explicit coexistence of wave and particle by separate variables (wavefunction + particle positions + quantum potential).





---

11. Recommended “equations of focus” for deeper study (concise list)

1. Schrödinger equation:


2. Superposition expansion:


3. Projection (selective collapse):


4. Kraus (general) map:


5. Lindblad master equation:


6. Wigner function:


7. Bohmian guidance + quantum potential:


8. Energy expectation change:


9. Total unitary model (system+apparatus):  (pre-decoupling).




---

12. Short answers to the specific practical concerns you raised

Does a collapse violate “same power”/energy? Not when the measurement is modeled as part of a closed unitary evolution including apparatus/environment. Any change in subsystem energy is compensated elsewhere. In the reduced description (tracing out apparatus) energy expectation can change — this is physical energy exchange, not a fundamental violation.

Can wave and particle be put in one equation? Yes in several senses:

Wigner/Moyal formalism yields a single function  whose marginals reproduce both wave amplitudes and particle probability densities.

Density-matrix + Kraus/Lindblad formalism yields a single mathematical framework for both coherent superpositions and decohered mixtures.

Bohmian equations explicitly pair wave dynamics (ψ) and particle positions into a deterministic set of coupled equations.


Is collapse fundamental or emergent? Standard quantum mechanics treats collapse as a postulate; modern approaches (decoherence + open systems) show collapse can be emergent from unitary dynamics plus environment entanglement. Interpretational options (Copenhagen, Many-Worlds, Bohmian, objective collapse models) differ here — the math above is neutral and shows how the “appearance” of collapse arises without violating global conservation laws.



---

13. Next concrete steps I can do immediately (pick any)

1. Produce a worked example: a two-level system prepped in superposition, measured in an energy basis; compute explicit  and model unitary measurement apparatus to show energy balance.


2. Generate a detailed derivation of Wigner→Moyal→classical limit with explicit computations for a Gaussian wavepacket.


3. Write a 10–30 page mathematical introduction (as you previously asked) focused on the equations above (detailed proofs, derivations, diagrams).


4. Provide code (Python/Mathematica) that simulates decoherence (spin-bath or oscillator bath) and plots density matrix decoherence and energy exchange.
