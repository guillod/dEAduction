-- import data.set
import tactic

-- dEAduction imports
import structures2
import definitions
import notations_definitions

-- General principles :
-- Type should be defined as parameters, in order to be implicit everywhere
-- other parameters are implicit in definitions, i.e. defined using '{}' (e.g. {A : set X} )
-- but explicit everywhere else, i.e. defined using '()' (e.g. (A : set X) )
-- each definition must be an iff statement (since it will be called with 'rw' or 'symp_rw')



local attribute [instance] classical.prop_decidable

---------------------------------------------
-- global parameters = implicit variables --
---------------------------------------------
section course
parameters {X Y Z: Type}

notation [parsing_only] P ` and ` Q := P ∧ Q
notation [parsing_only]  P ` or ` Q := P ∨ Q
notation [parsing_only]  ` not ` P := ¬ P
notation [parsing_only]  P ` implies ` Q := P → Q
notation [parsing_only]  P ` iff ` Q := P ↔ Q

notation [parsing_only]  x ` in ` A := x ∈ A
notation [parsing_only]  A ` cap ` B := A ∩ B
notation [parsing_only]  A ` cup ` B := A ∪ B
notation [parsing_only]  A ` subset ` B := A ⊆ B
notation [parsing_only]  `emptyset` := ∅


notation [parsing_only] P ` et ` Q := P ∧ Q
notation [parsing_only]  P ` ou ` Q := P ∨ Q
notation [parsing_only]  ` non ` P := ¬ P
notation [parsing_only]  P ` implique ` Q := P → Q
notation [parsing_only]  P ` ssi ` Q := P ↔ Q

notation [parsing_only]  x ` dans ` A := x ∈ A
notation [parsing_only]  A ` inter ` B := A ∩ B
notation [parsing_only]  A ` union ` B := A ∪ B
notation [parsing_only]  A ` inclus ` B := A ⊆ B
notation [parsing_only]  `vide` := ∅

open set

------------------
-- COURSE TITLE --
------------------
namespace theorie_des_ensembles
/- dEAduction
PrettyName
    Théorie des ensembles
-/


------------------------
-- COURSE DEFINITIONS --
------------------------
lemma definition.ssi {P Q : Prop} : (P ↔ Q) ↔ (P → Q) ∧ (Q → P) :=
begin
    exact iff_def
end
lemma definition.inclusion {A B : set X} : A ⊆ B ↔ ∀ {x:X}, x ∈ A → x ∈ B :=
begin
    exact iff.rfl
end

lemma definition.egalite_deux_ensembles {A A' : set X} :
(A = A') ↔ ( ∀ x, x ∈ A ↔ x ∈ A' ) :=
/- dEAduction
PrettyName
    egalité de deux ensembles
-/
begin
     exact set.ext_iff
end

lemma theorem.double_inclusion (A A' : set X) :
(A ⊆ A' ∧ A' ⊆ A) → A = A' :=
/- dEAduction
PrettyName
    Double inclusion
-/
begin
    exact set.subset.antisymm_iff.mpr
end

---------------
-- SECTION 1 --
---------------
namespace unions_et_intersections
-- variables unions_et_intersections --
variables {A B C : set X}

-----------------
-- DEFINITIONS --
-----------------
lemma definition.intersection_deux_ensembles {A B : set X} {x : X} :
x ∈ A ∩ B ↔ ( x ∈ A ∧ x ∈ B) :=
/- dEAduction
PrettyName
    Intersection de deux ensembles
-/
begin
    exact iff.rfl
end

lemma definition.intersection_quelconque_ensembles {I : Type} {E : I → set X}  {x : X} :
(x ∈ set.Inter (λ i, E i)) ↔ (∀ i:I, x ∈ E i) :=
/- dEAduction
PrettyName
    Intersection d'une famille d'ensembles quelconque
-/
begin
    exact set.mem_Inter
end

lemma definition.union_deux_ensembles  {A : set X} {B : set X} {x : X} :
x ∈ A ∪ B ↔ ( x ∈ A ∨ x ∈ B) :=
/- dEAduction
PrettyName
    Union de deux ensembles
-/
begin
    exact iff.rfl
end

lemma definition.union_quelconque_ensembles {I : Type} {E : I → set X}  {x : X} :
(x ∈ set.Union (λ i, E i)) ↔ (∃ i:I, x ∈ E i) :=
/- dEAduction
PrettyName
    Union d'une famille d'ensembles quelconque
-/
begin
    exact set.mem_Union
end


---------------
-- EXERCICES --
---------------
lemma exercise.union_distributive_inter : A ∩ (B ∪ C)  = (A ∩ B) ∪ (A ∩ C) :=
/- dEAduction
PrettyName
    Intersection avec une union
Description
    L'intersection est distributive par rapport à l'union
Tools->Logic
    $ALL -negate
Tools->ProofTechniques
    $ALL -contradiction
Tools->Definitions
    $UNTIL_NOW -union_quelconque_ensembles -intersection_quelconque_ensembles
Tools->Theorems
    double_inclusion
ExpectedVarsNumber
    X=3, A=1, B=1
-/
begin
    sorry,
end


lemma exercise.inter_distributive_union : A ∪ (B ∩ C)  = (A ∪ B) ∩ (A ∪ C) :=
/- dEAduction
PrettyName
    Union avec une intersection
Description
    L'union est distributive par rapport à l'intersection
-/
begin
    sorry
end

end unions_et_intersections


---------------
-- SECTION 2 --
---------------
namespace complementaire
-- variables complementaire --
variables  {A B : set X}
variables {I : Type} {E F : I → set X}
-- notation `∁`A := set.compl A

-----------------
-- DEFINITIONS --
-----------------
lemma definition.complement {A : set X} {x : X} : x ∈ set.compl A ↔ x ∉ A :=
/- dEAduction
PrettyName
    Complémentaire
-/
begin
    finish
end

--lemma definition.difference_d_ensembles {A B : set X} {x : X} : x ∈ B \ A ↔ (x ∈ B ∧ x ∉ A) :=
-- iff.rfl


---------------
-- EXERCICES --
---------------
lemma exercise.complement_complement : (set.compl (set.compl A)) = A :=
/- dEAduction
PrettyName
    Complémentaire du complémentaire
Description
    Tout ensemble est égal au complémentaire de son complémentaire
-/
begin
    sorry
end

lemma exercise.complement_union_deux :
set.compl (A ∪ B) = (set.compl A) ∩ (set.compl B) :=
/- dEAduction
PrettyName
    Complémentaire d'union I
Description
    Le complémentaire de l'union de deux ensembles égale l'intersection des complémentaires
-/
begin
    sorry
end

lemma exercise.complement_union_quelconque :
set.compl (set.Union (λ i, E i)) = set.Inter (λ i, set.compl (E i)) :=
/- dEAduction
PrettyName
    Complémentaire d'union II
Description
    Le complémentaire d'une réunion quelconque égale l'intersection des complémentaires
-/
begin
    sorry
end


lemma exercise.inclusion_complement_I :
A ⊆ B → set.compl B ⊆ set.compl A
:=
/- dEAduction
PrettyName
    Le passage au complémentaire renverse les inclusions, implication
Description
    Si A est inclus dans B, alors le complémentaire de A contient le complémentaire de B
-/
begin
    sorry
end

lemma exercise.inclusion_complement_II :
A ⊆ B ↔ set.compl B ⊆ set.compl A
:=
/- dEAduction
PrettyName
    Le passage au complémentaire renverse les inclusions, équivalence
Description
    Si A est inclus dans B, alors le complémentaire de A contient le complémentaire de B
-/
begin
    sorry
end

/- Autres : différence-/

end complementaire



-- Ajouter : 3. produit cartésien, 4. relations ?
-- comment définit-on un produit cartésien d'ensembles ?



---------------
-- SECTION 3 --
---------------
namespace applications_I
/- dEAduction
PrettyName
    Applications et opérations ensemblistes
-/


-- variables applications --

notation f `⟮` A `⟯` := f '' A
notation f `⁻¹⟮` A `⟯` := f  ⁻¹' A

variables  {A A': set X}
variables {f: X → Y} {B B': set Y}
variables {I : Type} {E : I → set X} {F : I → set Y}

-- a-t-on besoin de ceci ?
-- lemma theorem.egalite_fonctions : f = f' ↔ ∀ x : X, f(x) = f'(x) :=
--  function.funext_iff


-----------------
-- DEFINITIONS --
-----------------
lemma definition.image_directe (y : Y) : y ∈ f '' A ↔ ∃ x : X, x ∈ A ∧  f x = y :=
/- dEAduction -/
begin
    sorry
end

lemma definition.image_reciproque (x:X) : x ∈ f  ⁻¹' B ↔ f(x) ∈ B :=
/- dEAduction -/
begin
    sorry
end


---------------
-- EXERCICES --
---------------
lemma exercise.image_de_reciproque : f '' (f ⁻¹' B)  ⊆ B :=
begin
    sorry
end

lemma exercise.reciproque_de_image : A ⊆ f ⁻¹' (f '' A) :=
begin
    sorry
end

lemma exercise.image_reciproque_inter :  f ⁻¹'  (B∩B') = f ⁻¹'  (B) ∩ f ⁻¹'  (B') :=
begin
    sorry
end

lemma  exercise.image_reciproque_union  : f ⁻¹' (B ∪ B') = f ⁻¹' B ∪ f ⁻¹' B'
:=
begin
    sorry
end

-- set_option pp.width 100
lemma exercise.image_reciproque_inter_quelconque :
(f ⁻¹'  (set.Inter (λ i, F i))) = set.Inter (λ i, f ⁻¹' (F i))
:=
/- dEAduction
PrettyName
    Image réciproque d'une intersection quelconque
-/
begin
    sorry
end

/- Idem union quelconques -/

lemma exercise.image_inter_inclus_inter_images :
f '' (A∩A') ⊆ f '' (A) ∩ f '' (A')
:=
begin
    sorry
end


lemma exercise.reciproque_complementaire_I :
f ⁻¹' (set.compl B) ⊆ set.compl (f ⁻¹' B)
:=
/- dEAduction
PrettyName
    Image réciproque du complémentaire, inclusion
-/
begin
    sorry
end

lemma exercise.reciproque_complementaire_II :
f ⁻¹' (set.compl B) = set.compl (f ⁻¹' B)
:=
/- dEAduction
PrettyName
    Image réciproque du complémentaire, égalité
-/
begin
    sorry
end

end applications_I

----------------
-- SUBSECTION --
----------------
namespace applications_II
/- dEAduction
PrettyName
    Injections et surjections
-/

-- variables injections_surjections --
variables (f: X → Y) (g : Y → Z) (h : X → Z)

-----------------
-- DEFINITIONS --
-----------------
namespace definitions
/-
def injective {X Y : Type} (f₀ : X → Y) := ∀ x y : X, (f₀ x = f₀ y → x = y)
def surjective {X Y : Type} (f₀ : X → Y) := ∀ y : Y, ∃ x : X, f₀ x = y
def composition {X Y Z : Type} (g₀ : Y → Z) (f₀ : X → Y) := λx:X, g₀ (f₀ x)
def Identite {X : Type} := λ x:X, x

notation g `∘` f := composition g f
-/


lemma definition.injectivite :
injective f ↔ ∀ x y : X, (f x = f y → x = y)
:=
begin
    refl,
end

lemma definition.surjectivite :
surjective f ↔ ∀ y : Y, ∃ x : X, f x = y
:=
begin
    refl,
end

lemma definition.composition :
∀ x:X, composition g f x = g (f x)
:=
begin
    sorry
end

lemma definition.egalite_fonctions (f' : X → Y) :
f = f' ↔ ∀ x, f x = f' x :=
begin
    exact function.funext_iff,
end


lemma definition.Identite (f₀: X → X) :
f₀ = Identite ↔ ∀ x, f₀ x = x :=
begin
    apply definition.egalite_fonctions,
end

end definitions


---------------
-- EXERCICES --
---------------

---------------------
namespace composition
open applications_II.definitions

lemma exercise.composition_injections
(H1 : injective f) (H2 : injective g)
:
injective (composition g f)
:=
begin
    sorry
end

lemma exercise.composition_surjections
(H1 : surjective f) (H2 : surjective g) :
surjective (composition g f)
:=
begin
    sorry
end

lemma exercise.injective_si_coompo_injective
(H1 : injective (composition g f)) :
injective f
:=
begin
    sorry
end

lemma exercise.surjective_si_coompo_surjective
(H1 : surjective (composition g f)) :
surjective g
:=
begin
    sorry
end

lemma exercise.injective_ssi_inverse_gauche : (injective f) ↔
∃ F: Y → X, (composition F f) = Identite :=
begin
    sorry
end

lemma exercise.surjective_ssi_inverse_droite : (surjective f) ↔
∃ F: Y → X, (composition f F) = Identite :=
begin
    sorry
end

end composition

end applications_II

-----------------------------------
-----------------------------------
namespace exercices_supplementaires


-- relations : rel d'eq implique classes égales ou disjointes
-- les images réciproques des singletons forment une partition
-- bijective ssi inversible à g et d et inverses coincident


lemma exercise.exercice_ensembles_1
(A B : set X) :
A ∩ B = A ∪ B → A = B
:=
begin
    sorry
end



lemma exercise.exercice_ensembles_2
(A B C : set X) :
A ∩ B = A ∩ C ∧ (set.compl A) ∩ B = (set.compl A) ∩ C → B = C
:=
begin
    sorry
end



lemma exercise.exercice_ensembles_3
(A B C : set X) :
A ∩ B = A ∩ C ∧ A ∪ B = A ∪ C → B = C
:=
begin
    sorry
end

lemma exercise.exercice_ensembles_4
(A B : set X) :
A ⊆ B ↔ A ∩ B = A
:=
begin
    sorry
end

lemma exercise.complement_intersection_deux
(A B : set X):
set.compl (A ∩  B) = (set.compl A) ∪ (set.compl B)
:=
begin
    sorry
end

--def diff {X : Type} (A B : set X) := {x ∈ A | ¬ x ∈ B}
--notation A `\\` B := diff A B

-- def symmetric_difference {X : Type} (A B : set X) := (A ∪ B) \ (A ∩ B)
-- notation A `Δ` B := symmetric_difference A B

lemma definition.difference
(A B : set X) (x : X) :
x ∈ (A \ B) ↔ x ∈ A ∧ x ∉ B
:=
begin
    refl,
end


lemma definition.difference_symetrique
(A B : set X) :
(A Δ B) =  (A ∪ B) \ (A ∩ B)
:=
begin
    refl,
end


lemma exercise.difference_symetrique_1
(A B : set X) :
(A Δ B) = (A \ B) ∪ (B \ A)
:=
/- dEAduction
PrettyName
    Différence symétrique
-/
begin
    sorry
end


lemma exercise.difference_symetrique_2
(A B : set X) :
(A Δ B) = (B Δ A)
:=
begin
    sorry
end


lemma exercise.difference_symetrique_3
(A B C : set X) :
((A Δ B) Δ C) = (A Δ (B Δ C))
:=
begin
    sorry
end



notation `∃!` P := exists_unique P

lemma definition.existe_un_unique
(P : X → Prop) :
(∃! (λx,  P x)) ↔  (∃ x : X, (P x ∧ (∀ x' : X, P x' → x = x')))
:=
begin
    sorry
end

lemma exercise.difference_symetrique_4 :
∃! (λE : set X, ∀ A : set X, (A Δ E) = A) :=
begin
    sorry
end


lemma exercise.difference_symetrique_5 (A : set X) :
exists_unique (λA' : set X, (A Δ A') = set.univ)
:=
begin
    sorry
end

lemma exercise.difference_symetrique_6
(A B : set X) :
(A Δ B) = ∅ ↔ A = B
:=
begin
    sorry
end




-- applications
variable (f: X → Y)

lemma exercise.exercice_applications_1
(A B : set X) :
A ⊆ B → f '' A ⊆ f '' B
:=
begin
    sorry
end

lemma exercise.exercice_applications_2
(A B : set X) :
f '' (A ∪ B)  = f '' A ∪ f '' B
:=
begin
    sorry
end

open applications_II.definitions
lemma exercise.exercice_factorisation_I
(g : Y → Z) (h: X → Z) :
∃ f: X → Y, h = (composition g f) ↔ h '' set.univ ⊆ g '' set.univ
:=
begin
    sorry
end


lemma exercise.exercice_factorisation_II
(f : X → Y) (h: X → Z) :
∃ g: Y → Z, h = (composition g f) ↔ (∀ x y, (f x = f y → h x = h y))
:=
begin
    sorry
end



-- exoset ficall.pdf exos (140 bijections) 141 142 146



end exercices_supplementaires

end theorie_des_ensembles

end course