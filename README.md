# Crowded_Campus_and_Typo

## Name
Crowded_Campus_and_Typo

## Description

### Crowded Campus
The Campus Capacity Challenge: Allocating FIT2004 StudentsThe university administration faces an increasingly difficult class allocation dilemma driven by severe physical space limitations. The process of assigning unit classes to rooms and students to those classes is complex, relying on numerous interdependent variables: student enrollment projections, room resource suitability, room capacities, and the time constraints of both students and facilities.The New Constraint PolicyCurrently, physical space availability represents the primary bottleneck. Recognizing this, and noting student preferences for specific time slots, the space management team is implementing stricter classroom usage constraints. These new policy principles aim to maximize space efficiency:

Prime-Time Priority: During peak hours, a classroom must achieve near-maximum capacity, meaning student allocation must nearly fill the room.
Off-Peak Flexibility: Space allocation is less rigid during times that are less popular.
High-Demand Strictness: Classrooms with superior resources (and thus high unit popularity) face particularly strict occupancy limits.Furthermore, a key objective is student satisfaction, requiring the university to successfully place as many students as possible into classes scheduled during their most preferred times and days.

The Verification Problem:
The administration team conducted detailed analyses to define precise minimum occupancy rates for specific classrooms and time slots, based on the combined popularities. They produced a draft assignment of classes to rooms and times. However, the team quickly determined that manually verifying if a student allocation exists that satisfies all these constraints—particularly the occupancy and student satisfaction metrics—would be prohibitively difficult without computational assistance. As they lack an in-house computer scientist, they have sought external help.The specific request is to create an algorithm to verify the feasibility of their draft allocation for FIT2004 applied classes.

Input Specifications:
The problem is defined by the following inputs:
$n$ (Number of Students): A positive integer representing the student count (numbered $0$ to $n-1$).
$m$ (Number of Proposed Classes): A positive integer representing the count of draft classes (numbered $0$ to $m-1$).
timePreferences: A list of $n$ lists. Each inner list contains a permutation of the 20 available time slots ($0$ to $19$), ordered from the most preferred to the least preferred time slot for the corresponding student.
proposedClasses: A list of $m$ lists. For the $j$-th class, the list contains:The proposed time slot.The minimum student capacity required.The maximum student capacity permitted.
minimumSatisfaction: A positive integer (less than or equal to $n$) defining the required threshold for satisfied students.

Required Output & Constraints:
The task is to design an algorithm within a worst-case time complexity of $O(n^2)$ and an auxiliary space complexity of $O(n)$ that implements the function crowdedCampus(...).The function must find an allocation that simultaneously meets three criteria:
Completeness: Every single student is assigned to exactly one class.
Occupancy Compliance: Every proposed class adheres to its minimum and maximum student capacity constraints.
Satisfaction Goal: At least minimumSatisfaction students must be allocated to a class time that falls within their personal top 5 preferred time slots.The function must return a list representing the valid allocation (where allocation[i] is the class number for student $i$) or return None if no such allocation is possible.

### Typo
Typo Detection: Identifying AI-Generated ErrorsThe Levenshtein Distance (or Edit Distance) serves as a metric to quantify the difference between two words, defined by the minimum number of single-character edits (insertions, deletions, or substitutions) required to transform one word into the other. In this scenario, a programmer, having encountered an unhelpful AI that deliberately provides flawed Python code, is tasked with implementing a system to detect specific errors. The AI, acting as a troll, only introduces errors where the resulting word has a Levenshtein distance of exactly one from the correct word, and only through substitution (insertions and deletions are excluded).The programmer must therefore create a Python class, Bad_AI, designed for the efficient identification of words that are one substitution away from a suspected erroneous word.

The class structure requires two methods: one for initialization, which creates an efficient internal data structure without using dictionaries or hashing, and one for checking a word.
Input Specifications:
The following data characterizes the input provided to the class methods:
list_words: A list containing $N$ unique words. The longest word has $M$ characters, and the total character count across all words is $C$. Thus, $O(C)$ is less than or equal to $O(M \cdot N)$.
sus_word: A single word with $J$ characters.Character Set: All characters in both inputs are limited to lowercase letters (a–z), with no special characters, though the text mentions the potential presence of a period. Whitespaces are used for padding.
Order: The words in list_words are unique and cannot be assumed to be in any specific order. It is stated that words in both lists can be assumed to be sorted.

Output and Objective:
The method check_word(self, sus_word) must return a list of words from the initial list_words whose Levenshtein distance to sus_word is exactly 1, considering only single-character substitutions. An empty list, [], must be returned if no such words are found. The function may also return the result as a dictionary of words.

Complexity Requirements:
The implemented methods must adhere to the following worst-case complexity requirements:
init(self, list_words):
Time Complexity: $O(C)$Auxiliary Space Complexity: $O(C)$
check_word(self, sus_word):
Time Complexity: $O(J \cdot N) + O(X)$, where $X$ is the total number of characters returned in the result.

Auxiliary Space Complexity: $O(X)$.

## Installation
Latest Python.

## Usage
Run the Assignment2.py

## Support
fankasunarko@gmail.com

## Authors and acknowledgment
Many thanks to FIT2004 Monash University Clayton Semester 1 2025 Team for creating the project specification. 
Authors : Fauzanda Lathifanka Sunarko 
Email : fankasunarko@gmail.com

$# Project status
Complete.
