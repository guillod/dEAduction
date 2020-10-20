"""
# proofs.py : #ShortDescription #
    
    (#optionalLongDescription)

Author(s)     : Frédéric Le Roux frederic.le-roux@imj-prg.fr
Maintainer(s) : Frédéric Le Roux frederic.le-roux@imj-prg.fr
Created       : 07 2020 (creation)
Repo          : https://github.com/dEAduction/dEAduction

Copyright (c) 2020 the dEAduction team

This file is part of dEAduction.

    dEAduction is free software: you can redistribute it and/or modify it under
    the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    dEAduction is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
    more details.

    You should have received a copy of the GNU General Public License along
    with dEAduction.  If not, see <https://www.gnu.org/licenses/>.
"""

from deaduction.config.config import user_config, _

import deaduction.pylib.actions.utils as utils
from deaduction.pylib.actions import (InputType,
                                      MissingParametersError,
                                      WrongUserInput,
                                      action,
                                      format_orelse)
from deaduction.pylib.mathobj import (MathObject,
                                      Goal,
                                      get_new_hyp,
                                      give_global_name)

# turn logic_button_texts into a dictionary
proof_list= ['action_apply', 'proof_methods', 'new_object', 'assumption']
lbt = user_config.get('proof_button_texts').split(', ')
proof_button_texts = {}
for key, value in zip(proof_list, lbt):
    proof_button_texts[key] = value


@action(user_config.get('tooltip_proof_methods'),
        proof_button_texts['proof_methods'])
def action_use_proof_methods(goal: Goal, l: [MathObject],
                            user_input: [str] = []) -> str:
    # parameters
    allow_proof_by_sorry = user_config.getboolean('allow_proof_by_sorry')

    # 1st call, choose proof method
    if not user_input:
        choices = [('1', _("Case-based reasoning")),
                   ('2', _("Proof by contrapositive")),
                   ('3', _("Reductio ad absurdum"))]
        if allow_proof_by_sorry:
            choices.append(('4', _("Admit current sub-goal!")))
        raise MissingParametersError(InputType.Choice,
                                     choices,
                                     title="Choose proof method",
                                     output=_("Which proof method?")
                                     )
    # 2nd call, call the adequate proof method. len(user_input) = 1.
    else:
        method = user_input[0] + 1
        if method == 1:
            # if len(user_input) > 1:
            #     del user_input[0]   # we do not need this user_input anymore
            #     # but we need the next choice
            return method_cbr(goal, l, user_input)
        if method == 2:
            return method_contrapose(goal, l)
        if method == 3:
            return method_absurdum(goal, l)
        if method == 4:
            return method_sorry(goal, l)
    raise WrongUserInput


def method_cbr(goal: Goal, l: [MathObject], user_input: [str] = []) -> str:
    """
    Translate into string of lean code corresponding to the action
    
    :param l: list of MathObject arguments preselected by the user
    :return: string of lean code
    """
    possible_codes = []
    if len(l) == 0:
        # NB: user_input[1] contains the needed property
        if len(user_input) == 1:
            raise MissingParametersError(
                 InputType.Text,
                 title=_("cases"),
                 output=_("Enter the property you want to discriminate on:")
                                        )
        else:
            h0 = user_input[1]
            h1 = get_new_hyp(goal)
            h2 = get_new_hyp(goal)
            possible_codes.append(
                f"cases (classical.em ({h0})) with {h1} {h2}")
    else:
        h0 = l[0].info['name']
        h1 = get_new_hyp(goal)
        h2 = get_new_hyp(goal)
        possible_codes.append(
            f"cases (classical.em ({h0})) with {h1} {h2}")

    return format_orelse(possible_codes)


def method_contrapose(goal: Goal, l: [MathObject]) -> str:
    """
    Translate into string of lean code corresponding to the action
    
    :param l: list of MathObject arguments preselected by the user
    :return: string of lean code
    """
    possible_codes = []
    if len(l) == 0:
        if goal.target.math_type.node == "PROP_IMPLIES":
            possible_codes.append("contrapose")
    return format_orelse(possible_codes)


def method_absurdum(goal: Goal, l: [MathObject]) -> str:
    """
    Translate into string of lean code corresponding to the action
    
    :param l: list of MathObject arguments preselected by the user
    :return: string of lean code
    """
    possible_codes = []
    if len(l) == 0:
        new_h = get_new_hyp(goal)
        possible_codes.append(f'by_contradiction {new_h}')
    return format_orelse(possible_codes)


def method_sorry(goal: Goal, l: [MathObject]) -> str:
    """
    Close the current sub-goal by sending the 'sorry' code
    """
    possible_codes = ['sorry']
    return format_orelse(possible_codes)

def introduce_fun(goal: Goal, l: [MathObject]) -> str:
    """
    Translate into string of lean code corresponding to the action

If a hypothesis of form ∀ a ∈ A, ∃ b ∈ B, P(a,b) has been previously selected:
use the axiom of choice to introduce a new function f : A → B
and add ∀ a ∈ A, P(a, f(a)) to the properties

    :param l: list of MathObject arguments preselected by the user
    :return: string of lean code
    """
    possible_codes = []
    if len(l) == 1:
        h = l[0].info["name"]
        hf = get_new_hyp(goal)
        f = utils.get_new_fun()
        possible_codes.append(
            f'cases classical.axiom_of_choice {h} with {f} {hf}, dsimp at {hf}, dsimp at {f}')
    return format_orelse(possible_codes)


@action(user_config.get('tooltip_new_object'),
        proof_button_texts['new_object'])
def action_new_object(goal: Goal, l: [MathObject],
                      user_input: [str] = []) -> str:
    """
    Translate into string of lean code corresponding to the action

    Introduce new object\nIntroduce new subgoal:
transform the current target into the input target
and add this to the properties of the future goal.

    :param l: list of MathObject arguments preselected by the user
    :return: string of lean code
    """
    possible_codes = []
    if len(user_input) == 0:
        raise MissingParametersError(InputType.Choice,
                             [(_("Object"), _("Introduce a new object")),
                              (_("Sub-goal"), _("Introduce a new "
                                                "intermediate sub-goal")),
                              (_("New function"), _("Introduce a new "
                                                "function"))],
                             title="+",
                             output=_("Choose what to introduce:"))
    if user_input[0] == 0:  # choice = new object
        if len(user_input) == 1:  # ask for new object
            raise MissingParametersError(InputType.Text,
                                         title="+",
                                         output=_("Introduce new object:"))
        else:  # send code
            x = utils.get_new_var()
            h = get_new_hyp(goal)
            possible_codes.append(
                f"let {x} := {user_input[1]}, "
                f"have {h} : {x} = {user_input[1]}, refl, ")
    if user_input[0] == 1:  # new sub-goal
        if len(user_input) == 1:
            raise MissingParametersError(InputType.Text,
                                         title="+",
                                         output=_("Introduce new subgoal:"))
        else:
            h = get_new_hyp(goal)
            possible_codes.append(f"have {h} : ({user_input[1]}),")
    if user_input[0] == 2:
        return introduce_fun(goal, l)
    return format_orelse(possible_codes)




## APPLY


def apply_implicate(goal: Goal, l: [MathObject]):
    possible_codes = []
    h_selected = l[0].info["name"]
    possible_codes.append(f'apply {h_selected}')
    return possible_codes


def apply_implicate_to_hyp(goal: Goal, l: [MathObject]):
    """
    Try to apply last selected property on the other ones.
    :param l: list of 2 or 3 MathObjects
    :return:
    """
    possible_codes = []
    h_selected = l[-1].info["name"]
    x_selected = l[0].info["name"]
    h = get_new_hyp(goal)

    if len(l) == 2:
        # try with up to 4 implicit parameters
        possible_codes.append(f'have {h} := {h_selected} {x_selected}')
        possible_codes.append(f'have {h} := {h_selected} _ {x_selected}')
        possible_codes.append(f'have {h} := {h_selected} _ _ {x_selected}')
        possible_codes.append(f'have {h} := {h_selected} _ _ _ {x_selected}')
        possible_codes.append(f'have {h} := {h_selected} _ _ _ _ {x_selected}')

        possible_codes.append(f'have {h} := @{h_selected} {x_selected}')
        possible_codes.append(f'have {h} := @{h_selected} _ {x_selected}')
        possible_codes.append(f'have {h} := @{h_selected} _ _ {x_selected}')
        possible_codes.append(f'have {h} := @{h_selected} _ _ _ {x_selected}')
        possible_codes.append(
            f'have {h} := @{h_selected} _ _ _ _ {x_selected}')

    elif len(l) == 3:
        y_selected = l[1].info["name"]
        # try to apply "forall x,y , P(x,y)" to x and y
        possible_codes.append(
            f'have {h} := {h_selected} {x_selected} {y_selected}')
        possible_codes.append(
            f'have {h} := {h_selected} _ {x_selected} {y_selected}')
        possible_codes.append(
            f'have {h} := {h_selected} _ _ {x_selected} {y_selected}')
        possible_codes.append(
            f'have {h} := {h_selected} _ _ _ {x_selected} {y_selected}')
        possible_codes.append(
            f'have {h} := {h_selected} _ _ _ _ {x_selected} {y_selected}')

    return possible_codes


def apply_substitute(goal: Goal, l: [MathObject], user_input: [int]):
    """
    Try to rewrite the goal or the first selected property using the last
    selected property
    """
    possible_codes = []
    if len(l) == 1:
        heq = l[0]
    else:
        heq = l[-1]
    left_term = heq.math_type.children[0]
    right_term = heq.math_type.children[1]
    choices = [(left_term.format_as_utf8(),
            f'{left_term.format_as_utf8()} ← {right_term.format_as_utf8()}'),
            (right_term.format_as_utf8(),
            f'{right_term.format_as_utf8()} ← {left_term.format_as_utf8()}')]
            
    if len(l) == 1:
        h = l[0].info["name"]
        if len(user_input) > 0 and user_input[0] <= 1:
            if user_input[0] == 1:
                possible_codes.append(f'rw <- {h}')
            else:
                possible_codes.append(f'rw {h}')
        else:
            if goal.target.math_type.contains(left_term) and \
                    goal.target.math_type.contains(right_term):
                
                raise MissingParametersError(
                    InputType.Choice,
                    choices, 
                    title=_("Precision of substitution"),
                    output=_("Choose which one you want to replace"))
                 
            possible_codes.append(f'rw {h}')
            possible_codes.append(f'rw <- {h}')
    
    if len(l) == 2:
        h = l[0].info["name"]
        heq = l[-1].info["name"]
        if len(user_input) > 0 and user_input[0] <= 1:
            if user_input[0] == 1:
                possible_codes.append(f'rw <- {heq} at {h}')
            else:
                possible_codes.append(f'rw {heq} at {h}')
        else:     
            if l[0].math_type.contains(left_term) and \
                    l[0].math_type.contains(right_term):
                    
                raise MissingParametersError(
                    InputType.Choice,
                    choices, 
                    title=_("Precision of substitution"),
                    output=_("Choose what you want to replace"))
                
        possible_codes.append(f'rw <- {heq} at {h}')
        possible_codes.append(f'rw {heq} at {h}')

        h, heq = heq, h
        possible_codes.append(f'rw <- {heq} at {h}')
        possible_codes.append(f'rw {heq} at {h}')

    return possible_codes



def apply_function(goal: Goal, l: [MathObject]):
    possible_codes = []

    if len(l) == 1:
        raise WrongUserInput
    
    # let us check the input is indeed a function
    function = l[-1]
    if function.math_type.node != "FUNCTION":
        raise WrongUserInput
    
    f = function.info["name"]
    Y = l[-1].math_type.children[1]
    
    while (len(l) != 1):
        new_h = get_new_hyp(goal)
        
        # if function applied to equality
        if l[0].math_type.is_prop():
            h = l[0].info["name"]
            possible_codes.append(f'have {new_h} := congr_arg {f} {h}')
            
        # if function applied to element x:
        # create new element y and new equality y=f(x)
        else:
            x = l[0].info["name"]
            y = give_global_name(goal=goal,
                    math_type=Y,
                    hints=[Y.info["name"].lower()])
            possible_codes.append(f'set {y} := {f} {x} with {new_h}')
        l = l[1:]
    return format_orelse(possible_codes)


@action(user_config.get('tooltip_apply'),
        proof_button_texts['action_apply'])
def action_apply(goal: Goal, l: [MathObject], user_input: [str] = []):
    """
    Translate into string of lean code corresponding to the action
    Function explain_how_to_apply should reflect the actions

    Apply last selected item on the other selected items

    :param l:   list of MathObject arguments preselected by the user
    :return:    string of lean code
    """
    possible_codes = []

    if len(l) == 0:
        raise WrongUserInput  # n'apparaîtra plus quand ce sera un double-clic

    # if user wants to apply a function
    if not l[-1].math_type.is_prop():
        return apply_function(goal, l)

    # determines which kind of property the user wants to apply
    math_type = l[-1].math_type
    quantifier = l[-1].math_type.node
    if math_type.can_be_used_for_substitution():
        if len(l) == 1 or (len(l) > 1 and l[0].math_type.is_prop()):
            possible_codes.extend(
                apply_substitute(goal, l, user_input))

    if quantifier == "PROP_IMPLIES" or quantifier == "QUANT_∀":
        if len(l) == 1:
            possible_codes.extend(apply_implicate(goal, l))
        if len(l) == 2 or len(l) == 3:
            possible_codes.extend(apply_implicate_to_hyp(goal, l))

    return format_orelse(possible_codes)


################################
# Captions for 'APPLY' buttons #
################################

applicable_nodes = {'FUNCTION',  # to apply a function
                    'PROP_EQUAL', 'PROP_IFF', 'QUANT_∀',  # for substitution
                    'PROP_IMPLIES'  # TODO: add 'QUANT_∃'
                    }


def is_applicable(math_object) -> bool:
    """
    True if math_object may be applied
    (--> an 'APPLY' button may be created)
    """
    return math_object.math_type.node in applicable_nodes


def explain_how_to_apply(math_object: MathObject, dynamic=False, long=False) \
        -> str:
    """
    Provide explanations of how the math_object may be applied
    (--> to serve as tooltip or help)
    :param math_object:
    :param dynamic: if False, caption depends only on main node
    :param long: boolean
    TODO: implement dynamic and long tooltips
    """
    if not is_applicable(math_object):
        return None

    node = math_object.math_type.node
    if node == 'FUNCTION':
        caption = _("Apply function to an element or an equality")

    if node == 'PROP_EQUAL':
        caption = _("Substitute in selected property")


    if node == 'PROP_IFF':
        caption = _("Substitute in selected property")


    if node == 'QUANT_∀':
        # todo: test for substitution
        caption = _("Apply to selected object")


    if node == 'PROP_IMPLIES':
        caption = _("Apply to selected property, or to change the goal")

    return caption
    
    

@action(user_config.get('tooltip_assumption'),
        proof_button_texts['assumption'])
def action_assumption(goal: Goal, l: [MathObject]) -> str:
    """
    Translate into string of lean code corresponding to the action
    
    :param l: list of MathObject arguments preselected by the user
    :return: string of lean code
    """

    possible_codes = []
    if len(l) == 0:
        possible_codes.append('assumption')
        possible_codes.append('contradiction')
        if goal.target.math_type.node == "PROP_EQUAL":
            if goal.target.math_type.children[0] == \
                    goal.target.math_type.children[1]:
                possible_codes.append('refl')
        possible_codes.append('ac_reflexivity')
        possible_codes.append('apply eq.symm, assumption')
        possible_codes.append('apply iff.symm, assumption')
    if len(l) == 1:
        possible_codes.append(f'apply {l[0].info["name"]}')
    return format_orelse(possible_codes)


# @action(_("Proof by induction"))
# def action_induction(goal : Goal, l : [MathObject]):
#    raise WrongUserInput
