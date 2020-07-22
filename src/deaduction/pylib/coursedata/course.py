"""
# course.py : provide the class Course
    
    Provide the class Course,
    and an instantiation method for Course object
    by getting informations from a lean file


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

from collections import OrderedDict
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import List
import deaduction.pylib.logger as logger
from deaduction.pylib.actions.actiondef import Action
from deaduction.pylib.coursedata.exercise import (Exercise, Definition,
                                                  Theorem, Statement)

@dataclass
class Course:
    outline: OrderedDict  # todo: typing OrderedDict
    # keys = lean complete namespaces,
    # values = corresponding plain language namespace
    # e. g. section_dict["set_theory.unions_and_intersections"] =
    # "Unions and intersections"
    statements: List[Statement]  # ORDERED list of all Statements,
    # including exercises
    file_content: str

    def extract_exercise(self):
        """
        extract all the exercises from the statements list
        """
        statements = self.statements
        exercises_list = [item for item in statements if isinstance(item,
                                                                    Exercise)]
        return exercises_list

    @classmethod
    def from_directory(cls, course_dir_path: Path):
        """
        instantiate a Course object by parsing every lean files
        in course_dir_path
        data fields to be parsed must start with "/- dEAduction"
        and end with "-/"

        :param course_dir_path: name of directory
        """
        # TODO: enable multiple exercises files ?
        log = logging.getLogger("Course initialisation")
        statements = []
        #        definitions = []
        #        theorems = []
        outline = {}
        # parse first exercise file in directory
        files = [file for file in course_dir_path.iterdir()]
        exo_files = [file for file in course_dir_path.iterdir() if \
                     str(file.name).startswith("exercise")]
        if len(exo_files) >= 1:
            file = exo_files[0]
            if len(exo_files) > 1:
                log.warning("Found more than one exercises files, parse one")
        else:
            file = files[0]
            if len(files) > 1:
                log.warning("Found more than one files, parse only one")

        log.info(f"Parsing file {file}")
        file_content = file.read_text()
        lines = file_content.splitlines()
        global_parsing = ""
        # possible values = "namespace", "statement", "exercise"
        data_parsing = ""
        # possible values = "", "field name", "<field name>"
        line_counter = 0
        indent = 0
        data = {"Section": None, "Tools->Logic": None,
                "Tools->Definitions": None, "Tools->Theorems": None,
                "Tools->Exercises": None, "Tools->Statements": None,
                "Tools->Magic": None, "Tools->ProofTechniques": None,
                "ExpectedVarsNumber": None, "text_book_identifier": None,
                "current_namespaces": []}
        for line in lines:
            line_counter += 1
            log.debug(f"Parsing line {line_counter}")
            log.debug(f"global_parsing: {global_parsing}, data_parsing: "
                      f"{data_parsing}")
            # data_parsing starts after a field_name_parsing
            # and goes on till the indentation stops
            if line.startswith("/- dEAduction"):
                data_parsing = "field name"
                # next line will be a field name
                continue
            elif data_parsing not in ["", "field name"]:
                data_parsing, indent = data_parse(data, data_parsing, indent,
                                                  line)
                log.debug(
                    f"data: {[(key, data[key]) for key in data.keys()]}")
            # note that previous lines may result in data_parsing="field name"
            # next line IS NOT elif
            if data_parsing == "field name":
                data_parsing = line.strip()
                log.info(f"get field name {data_parsing}")
                data[data_parsing] = ""
                continue
            elif line.endswith("-/"):
                # end of data_parsing
                log.info(f"Field content: {data[data_parsing]}")
                data_parsing = ""
                if global_parsing != "":
                    end_global_parsing(data,
                                       global_parsing, line_counter,
                                       outline, statements)
                    global_parsing = ""
                continue
            else:
                # treatment of namespaces
                global_parsing = namespace_parse(data, global_parsing, line,
                                                 line_counter, outline,
                                                 statements)
                # treatment of exercises
                global_parsing = statement_parse(data, global_parsing, line,
                                                 line_counter, outline,
                                                 statements)
        # Creating the course
        return cls(outline, statements)


def data_parse(data, data_parsing, indent, line):
    """
    """
    log = logging.getLogger("Course initialisation")
    new_indent = indentation(line)
    if new_indent != 0 and indent != 0 and new_indent != indent:
        log.warning("indentation error")
    if new_indent != 0:  # fill the field
        if data[data_parsing] != "":
            data[data_parsing] += " "
        data[data_parsing] += line.strip()
        if data[data_parsing].endswith("-/"):
            data[data_parsing] = data[data_parsing][:-2]
    elif new_indent == 0 and not line.endswith("-/"):
        # end of field, search for next field
        log.info(f"Field content: {data[data_parsing]}")
        data_parsing = "field name"
    log.debug(f"data: {[(key, data[key]) for key in data.keys()]}")
    return data_parsing, new_indent


def end_global_parsing(data, global_parsing,
                       line_counter, outline, statements):
    """
    This function is called whenever global_parsing is muted from something
    to nothing or something else. This is where statements are created,
    and added to the statements list,
    and namespaces are added to the outline of the course

    :param data:
    :param global_parsing:
    :param line_counter:
    :param outline:
    :param statements:
    :return:
    """
    log = logging.getLogger("Course initialisation")
    if global_parsing == "namespace":
        whole_namespace = ".".join(data["current_namespaces"])
        if whole_namespace not in outline.keys():
            if data["Section"] is None:
                # compute plain name from Lean name
                data["Section"] = \
                    data["current_namespaces"][-1].replace("_",
                                                           " ").capitalize()
        if data["Section"] is not None:
            outline[whole_namespace] = data["Section"]
        log.info(f"Namespace {whole_namespace},text: {data['Section']}")
        data["Section"] = None
    elif global_parsing == "statement":
        log.warning("unable to detect end of statement (':=')")
    elif global_parsing == "StatementMetadata":
        # creation of the Statement
        if data["lean_name"].startswith("exercise"):
            data["lean_line_number"] = line_counter
            log.info(f"creating exercise from data {data}")
            exercise = Exercise.from_parser_data(data, statements)
            statements.append(exercise)
        elif data["lean_name"].startswith("definition"):
            log.info(f"creating definition from data {data}")
            definition = Definition.from_parser_data(data)
            statements.append(definition)
        elif data["lean_name"].startswith("theorem"):
            log.info(f"creating theorem from data {data}")
            theorem = Theorem.from_parser_data(data)
            statements.append(theorem)


def namespace_parse(data, global_parsing, line,
                    line_counter, outline, statements):
    # namespace_parsing starts at "namespace",
    # ends at first "-/" or "lemma exercise."
    log = logging.getLogger("Course initialisation")
    if line.startswith("namespace"):
        end_global_parsing(data,
                           global_parsing, line_counter,
                           outline, statements)
        global_parsing = "namespace"
        namespace = line.split()[1]
        data["current_namespaces"].append(namespace)
        whole_namespace = ".".join(data["current_namespaces"])
        log.info(f"Parsing namespace {whole_namespace}")
    elif line.startswith("end") and len(line.split()) > 1:
        if line.split()[1] == data["current_namespaces"][-1]:
            # closing namespace
            data["current_namespaces"].pop()
    return global_parsing


def statement_parse(data, global_parsing, line,
                    line_counter, outline, statements):
    # statement_parsing starts at "lemma exercise.", ends at ":="
    # then exercise_parsing starts, and it ends at "-/"
    log = logging.getLogger("Course initialisation")
    if line.startswith("lemma exercise.") \
            or line.startswith("lemma definition.") \
            or line.startswith("lemma theorem."):
        if global_parsing != "":
            end_global_parsing(data,
                               global_parsing, line_counter,
                               outline, statements)
        global_parsing = "statement"
        words = line.split()
        data["lean_name"] = words[1]
        log.info(f"Parsing statement {data['lean_name']}")
        line = " ".join(words[2:])  # suppress the lemma declaration
        data["lean_variables"], _, line = line.rpartition(" : ")
        # todo: not very robust, to be improved
        data["lean_statement"] = ""
        data["PrettyName"] = None
        data["Description"] = None
        data["Tools->Logic"] =  None
        data["Tools->Magic"] =  None
        data["Tools->ProofTechniques"] = None
        data["Tools->Definitions"] =  None
        data["Tools->Theorems"] =  None
        data["Tools->Exercises"] =  None
        data["Tools->Statements"] = None
        # By default the other fields are as for the previous exercise
    if global_parsing == "statement":
        data["lean_statement"] += line.strip()
        if line.strip().endswith(":="):
            log.info("parsing statement data")
            data["lean_statement"] = data["lean_statement"][:-2]
            global_parsing = "StatementMetadata"
    return global_parsing


def indentation(line: str) -> int:
    """
    Compute the number of space at the beginning of line
    """
    i = 0
    while line[i] == " ":
        i += 1
    return i


if __name__ == "__main__":
    logger.configure()

    course_dir_path = Path(
        '/Users/leroux/Documents/PROGRAMMATION/LEAN/LEAN_TRAVAIL/dEAduction'
        '-lean/src/snippets/test')
    #    ex_file = 'exercises_test.lean'
    my_course = Course.from_directory(course_dir_path)
    print("My course:")
    print("List of statements:")
    count_ex= 0
    for statement in my_course.statements:
        if isinstance(statement, Exercise):
            count_ex += 1
            print(f"Exercise n°{count_ex}: {statement.pretty_name}")
        elif isinstance(statement, Definition):
            print(f"Definition {statement.pretty_name}")
        elif isinstance(statement, Theorem):
            print(f"Theorem {statement.pretty_name}")
        for key in statement.__dict__.keys():
            print(f"    {key}: {statement.__dict__[key]}")
    print('Sections:')
    for key in my_course.outline.keys():
        print(f"    {key}: {my_course.outline[key]}")
    print("Statements list :")
    for item in my_course.statements:
        print(item.lean_name)
    print("Exercises list with statements :")
    for item in my_course.statements:
        if isinstance(item, Exercise):
            print(item.lean_name)
            for st in item.available_statements:
                print("    " + st.lean_name)
