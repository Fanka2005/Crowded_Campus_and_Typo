import math
########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# QUESTION 1 #

def crowdedCampus(n: int, m: int, timePreferences: list[list], proposedClasses: list[list], minimumSatisfaction: int) -> list|None:
    """
		Function description: This function determines the allocation of each student to a proposed class that fullfill the following requirements : 
                                - Each student is allocated to exactly one class.
                                - Each proposed class satisfies its space occupancy constraints.
                                - At least minimumSatisfaction students get allocated to classes with class times that are within their top 5 preferred time slots.

		Approach description: This function will first use reduced_circular_demand_lowerbound_graph() function to models the relationship of student time preferences and proposed class using circular demand with lower bound network flow graph. 
                                The circular demand with lower bound network flow graph is then reduced until it becomes a regular network flow graph. The regular network flow graph will then be turn into an augmented graph. All of this is done in reduced_circular_demand_lowerbound_graph().
                                This function then run a modified ford-fulkerson algorithm implemented with depth first search (modified_ford_fulkerson()) throughout the regular network flow graph, and record the flow and destination of each edge.
                                The output of the modified_ford_fulkerson() is a max-flow graph.
                                This function will then run student_allocation() function to record every student allocation from the max-flow graph, the student allocation is indicated with an edge that have a flow of 0.
                                Furthermore, student_allocation() will also check whether it fullfill the following requirements : 
                                - Each student is allocated to exactly one class.
                                - Each proposed class satisfies its space occupancy constraints.
                                - At least minimumSatisfaction students get allocated to classes with class times that are within their top 5 preferred time slots.

                                
		Input: 
			n (int) : A positive integer n denoting the number of students to be allocated to FIT2004 applied classes.
            m (int) : A positive integer m denoting the number of proposed FIT2004 applied classes in the draft.

            timePreferences (list[list]) : A list of lists timePreferences of outer length n. For i ∈ 0, 1, . . . , n - 1, timePreferences[i] contains a permutation of the elements of set {0, 1, . . . , 19} to indicate the time slot preferences of student i. 
                                            The time slots in timePreferences[i] appear in order of preference, with the time slot that student i likes the most appearing first.

            proposedClasses (list[list]) : A list of lists proposedClasses of outer length m. For j ∈ 0, 1, . . . , m - 1: proposedClasses[j][0] denotes the proposed time slot for the j-th class. Potentially, there can be multiple FIT2004 applied classes running in parallel.
                                            proposedClasses[j][1] and proposedClasses[j][2] are positive integers that denote respectively, the minimum and maximum number of students that can be
                                            allocated to the j-th class to satisfy the space occupancy constraints.
                
            minimumSatisfaction (int) : A positive integer minimumSatisfaction. It holds that minimumSatisfaction ≤ n.

		Output: list| None :  - In case no allocation satisfying all constraints exists,it return None (i.e.,Python NoneType).
                              - A list allocation of length n containing exactly one possible allocation of the students to the classes that satisfies all constraints. For i ∈ 0, 1, . . . , n-1,
                                allocation[i] denotes the class number to which student i would be allocated.
		
		Time complexity: O(n*n), where n is the number of students to be allocated to FIT2004 applied classes.

		Time complexity analysis : Given n is the number of students to be allocated to FIT2004 applied classes:
                                    - Time : O(n) -> This function will first use reduced_circular_demand_lowerbound_graph() function to models the relationship of student time preferences and proposed class using circular demand with lower bound network flow graph. 
                                                        The circular demand with lower bound network flow graph is then reduced until it becomes a regular network flow graph.
                                                        The regular network flow graph will then be turn into an augmented graph. All of this is done in reduced_circular_demand_lowerbound_graph().
                                    - Time : O(n*n) ->  This function then run a modified ford-fulkerson algorithm implemented with depth first search (modified_ford_fulkerson()) throughout the regular network flow graph, and record the flow and destination of each edge.
                                                            The output of the modified_ford_fulkerson() is a max-flow graph.
                                    - Time : O(n) -> This function will then run student_allocation() function to record every student allocation from the max-flow graph, the student allocation is indicated with an edge that have a flow of 1.
                                                        Furthermore, student_allocation() will also check whether it fullfill the following requirements : 
                                                        - Each student is allocated to exactly one class.
                                                        - Each proposed class satisfies its space occupancy constraints.
                                                        - At least minimumSatisfaction students get allocated to classes with class times that are within their top 5 preferred time slots.
                                    
                                    Therefore the final time complexity is : O(n*n)


		Auxilary Space complexity: O(n), where n is the number of students to be allocated to FIT2004 applied classes.

        Auxilary Space complexity Analysis: Given n is the number of students to be allocated to FIT2004 applied classes:
                                    - Auxilary Space : O(n) -> This function will first use reduced_circular_demand_lowerbound_graph() function to models the relationship of student time preferences and proposed class using circular demand with lower bound network flow graph. 
                                                        The circular demand with lower bound network flow graph is then reduced until it becomes a regular network flow graph.
                                                        The regular network flow graph will then be turn into an augmented graph. All of this is done in reduced_circular_demand_lowerbound_graph().
                                    - Auxilar Space : O(n) ->  This function then run a modified ford-fulkerson algorithm implemented with depth first search (modified_ford_fulkerson()) throughout the regular network flow graph, and record the flow and destination of each edge.
                                                            The output of the modified_ford_fulkerson() is a max-flow graph.
                                    - Auxilar Space : O(n) -> This function will then run student_allocation() function to record every student allocation from the max-flow graph, the student allocation is indicated with an edge that have a flow of 1.
                                                        Furthermore, student_allocation() will also check whether it fullfill the following requirements : 
                                                        - Each student is allocated to exactly one class.
                                                        - Each proposed class satisfies its space occupancy constraints.
                                                        - At least minimumSatisfaction students get allocated to classes with class times that are within their top 5 preferred time slots.
                                    
                                    Therefore the final time complexity is : O(n)

	"""
    # Check whether n is less than m, if it is that means the proposed class allocation must be invalid and will return None.
    # Therefore for the following time and space complexity, we will assume n = m for the upper bound.
    # Time : O(1), Space : O(1)
    if n < m:
        return None

    # Define the number of time slot available, in this case is 20, and therefore t = 20 (constant), where t is the total number of time slot available.
    total_time_slot = 20

    # This function is use to models the relationship of student time preferences, the time slot, and proposed class using circular demand with lower bound network flow graph. 
    # The circular demand with lower bound network flow graph is then reduced until it becomes a regular network flow graph. The regular network flow graph will then be turn into an augmented graph.
    # Time complexity: O(n*t + m*t), Space Complexity O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    # Because the upperbound of m is equal to n
    # And the time slot t is constant 20, Therefore :
    # Final Time complexity: O(n), Final Space Complexity O(n), where n is the number of students to be allocated to FIT2004 applied classes
    graph = reduced_circular_demand_lowerbound_graph(n, m, total_time_slot, timePreferences, proposedClasses)

 
    if graph == None:
        return None
    
    # This function is use to recursively find an augmented path from the super source nodes to the sink nodes and update the flow of both the forward edges and backward edges using depth first search algorithm in the reduced augmented circular demand with lower bound network flow graph until it reaches its maxmum flow.
    # Primarly, this function is used to find the optimal flow network of the reduced augmented circular demand with lower bound network flow graph.
    # Time complexity: O(n*(n*t + m*t)), Space Complexity : O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    # Because the upperbound of m is equal to n
    # And the time slot t is constant 20, Therefore :
    # Final Time complexity: O(n*n), Final Space Complexity O(n), where n is the number of students to be allocated to FIT2004 applied classes
    source = len(graph)-1
    target = len(graph)-2
    graph = modified_ford_fulkerson(graph ,source, target, n, m, total_time_slot, proposedClasses)
 
    # This function is used to determine the validity of the proposedClassess, whether or not there is a valid student allocation that satisfy all constraints, which are : 
    #                           • Each student is allocated to exactly one class.
    #                           • Each proposed class satisfies its space occupancy constraints.
    #                           • At least minimumSatisfaction students get allocated to classes with class times that are
    #                               within their top 5 preferred time slots.
    #                           If it does meet all constraints, then it will note/record all of the student that have been allocated to a class into the student allocated list, including which class they are allocated to.
    #                           This function uses the filled network flow graph to determine which student is allocated to which class.
    # Time complexity: O(m*t*n), Space Complexity : O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    # Because the upperbound of m is equal to n
    # And the time slot t is constant 20, Therefore :
    # Final Time complexity: O(n), Final Space Complexity O(n), where n is the number of students to be allocated to FIT2004 applied classes

    student_allocated = student_allocation(total_time_slot, timePreferences, proposedClasses, minimumSatisfaction, graph)
    return student_allocated
    

class Edge:
    """
		Class description: This class is used to define an edge as an object with the following attribute:
                            self.to = edge destination node
                            self.capacity = capacity of the edge
                            self.flow = Forward flow of the edge
                            self.reverse=  The pointer to the edge object of the reverse edge
                            self.time_slot = The time corelated to the destination node. 

        Input: 
                destination (Edge) : The edge destination node
                time_slot (int) : The time corelated to the destination node. 
                Capacity (int) : Capacity of the edge
                forward_flow : Forward flow of the edge
                
        Output: None
            
        Time complexity: O(1)

        Time complexity analysis :  Because this class only create an edge object and assign a constant value to a constant number of variable, therefore its O(1).

        Space complexity: O(1)

        Space complexity analysis:  Because this class only create an edge object and assign a constant value to a constant number of variable, therefore its O(1).
     
    """
    def __init__(self, destination, time_slot, capacity, forward_flow):
        """
            Function description: This function initialise and defines the following attribute : 
                                    self.to = edge destination node
                                    self.capacity = capacity of the edge
                                    self.flow = Forward flow of the edge
                                    self.reverse=  The pointer to the edge object of the reverse edge
                                    self.time_slot = The time corelated to the destination node.  
                    
            Input: 
                destination (Edge) : The edge destination node
                time_slot (int) : The time corelated to the destination node. 
                Capacity (int) : Capacity of the edge
                forward_flow : Forward flow of the edge
                
            Output: None
                
            Time complexity: O(1)

            Time complexity analysis :  Because this function only assign a constant value to a constant number of variable, therefore its O(1).

            Space complexity: O(1)

            Space complexity analysis:  Because this function only assign a constant value to a constant number of variable, therefore its O(1).
        """
        self.to = destination
        self.capacity = capacity
        self.flow = forward_flow
        self.reverse= None
        self.time_slot = time_slot

  
def reduced_circular_demand_lowerbound_graph(n: int, m: int, total_time_slot: int, timePreferences: list[list], proposedClasses: list[list]) -> list[list]|None:
    """
		Function description: This function is use to models the relationship of student time preferences, the time slot, and proposed class using circular demand with lower bound network flow graph. 
                                The circular demand with lower bound network flow graph is then reduced until it becomes a regular network flow graph. The regular network flow graph will then be turn into an augmented graph.

		Approach description: In the following, an "edge" refers to a forward directed edge, while a "reverse edge" refers to a backward directed edge.
                                This function will first create the vertices/nodes for the all of the proposed class nodes, time slot nodes, student nodes, the source nodes, the sink nodes, and the super sink nodes.
                                It will then models the relationship of student time preferences and proposed class in a form of an edge from the class nodes to student nodes. 
                                The satisified student will have an edge from every time node where the class time is in that student top 5 time preferences list to the respective satisfied student nodes and also a reverse edge. 
                                    The edge will have a flow of 0 and reverse edge will have a flow of 1, both will have a capacity of 1.
                                The non satisified student will have an edge from every time node where the class time is NOT in that student top 5 time preferences list to the respective non satisfied student nodes and also a reverse edge. 
                                    The edge will have a flow of 0 and reverse edge will have a flow of 1, both will have a capacity of 1.
                                The time nodes will have an incoming edge from every class node where the class time is equal to that of the time nodes and also a reverse edge. 
                                    The edge will have a flow of 0 and reverse edge will have a flow of (maximum capacity - minimum capacity) of that specific proposed class, both will have a capacity of the proposed class maximum capacity.
                                It will also Add forward edges and reverse edges from augment/super source node to every time nodes for the reduced demands. The forward edge will have a flow of 0, while the backward edge will have a flow of the total minimum capacity of the class nodes that is connected.
                                    The capacity of both edge will be total minimum capacity of the class nodes that is connected.
                                This function will then create an edge and reverse edge from the source nodes to every class nodes with a capacity of: residual capacity = maximum class capacity - minimum class capacity.
                                    The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.
                                Next, it wll Check whether the number of student is less than the sum of all classes minimum capacity constraint or the number of student is greater than the sum of all classes maximum capacity constraint
                                    This is a first layer check whether it is feasible to satisfy all constraints.
                                It will then create an edge and reverse edge from super source/augmented source nodes to source nodes with a capacity of : the number of student - (total_sink_capacity = the sum of every minimum class capacity).
                                    The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.
                                Lastly, it will create an edge and reverse edge from the all of the student nodes to the sink node with a capacity of 1.
                                    The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.

                                The graph flow is : Super source/augmented source node -> source node   -> class nodes -> time nodes --------------------------------> satisfied student nodes -> Sink node
                                                                                                        --------------------^        -> non satisfied student ndoes ------^ 
                                
		Input: 
			n (int) : A positive integer n denoting the number of students to be allocated to FIT2004 applied classes.
            m (int) : A positive integer m denoting the number of proposed FIT2004 applied classes in the draft.
            total_time_slot (int) : A positive integer t denoting the total number of time slot available.
            
            timePreferences (list[list]) : A list of lists timePreferences of outer length n. For i ∈ 0, 1, . . . , n - 1, timePreferences[i] contains a permutation of the elements of set {0, 1, . . . , 19} to indicate the time slot preferences of student i. 
                                            The time slots in timePreferences[i] appear in order of preference, with the time slot that student i likes the most appearing first.

            proposedClasses (list[list]) : A list of lists proposedClasses of outer length m. For j ∈ 0, 1, . . . , m - 1: proposedClasses[j][0] denotes the proposed time slot for the j-th class. Potentially, there can be multiple FIT2004 applied classes running in parallel.
                                            proposedClasses[j][1] and proposedClasses[j][2] are positive integers that denote respectively, the minimum and maximum number of students that can be
                                            allocated to the j-th class to satisfy the space occupancy constraints.
                

		Output: (list[list]|None) : an adjacency list to represent the augment reduced cicular demand with lowerbound network flow graph.

        IMPORTANT : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        !!!! 
            For the following time and space complexity,
                This function is independent from the assingnment specification constraints, the time and space complexity is dependent on the input. Thus, the calculation of time and space complexity is not dependent on the assingnment specification constraints.
                The final time and space complexity considering the assingnment specification constraints will be calculated and explained in crowdedCampus() function.
        !!!!

        !!!!
            Every time and space complexity that is present in this function referes to their worst case time and space complexity.
        !!!!
		
		Time complexity: O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.

		Time complexity analysis : Given n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
                                    - Time : O(n+m+t) -> This function will first create the vertices/nodes for the all of the proposed class nodes, time slot nodes (which represent the time from 0-19, 20 nodes constant), student nodes, the source nodes, the sink nodes, and the super sink nodes.
                                    - Time : O(n*t) ->  It will then models the relationship of student time preferences and proposed class in a form of an edge from the class nodes to student nodes. 
                                                        The satisified student will have an edge from every time node where the class time is in that student top 5 time preferences list to the respective satisfied student nodes and also a reverse edge. 
                                                            The edge will have a flow of 0 and reverse edge will have a flow of 1, both will have a capacity of 1.
                                                        The non satisified student will have an edge from every time node where the class time is NOT in that student top 5 time preferences list to the respective non satisfied student nodes and also a reverse edge. 
                                                            The edge will have a flow of 0 and reverse edge will have a flow of 1, both will have a capacity of 1.
                                    - Time : O(t*m) ->  The time nodes will have an incoming edge from every class node where the class time is equal to that of the time nodes and also a reverse edge. 
                                                            The edge will have a flow of 0 and reverse edge will have a flow of (maximum capacity - minimum capacity) of that specific proposed class, both will have a capacity of the proposed class maximum capacity.
                                    - Time : O(m) ->  This function will then create an edge and reverse edge from the source nodes to every class nodes with a capacity of: residual capacity = maximum class capacity - minimum class capacity.
                                                        The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.
                                    - Time : O(1) ->  Next, it wll Check whether the number of student is less than the sum of all classes minimum capacity constraint or the number of student is greater than the sum of all classes maximum capacity constraint
                                                        This is a first layer check whether it is feasible to satisfy all constraints.
                                    - Time : O(1) ->It will then create an edge and reverse edge from super source/augmented source nodes to source nodes with a capacity of : the number of student - (total_sink_capacity = the sum of every minimum class capacity).
                                                        The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.
                                    - Time : O(n) ->  Lastly, it will create an edge and reverse edge from the all of the student nodes to the sink node with a capacity of 1.
                                                        The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.


                                    Therefore, the final time complexity is : O(n+m+t + t*n + t*m + m + 1 + n) = O(n+m)

		Space complexity: O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.

        Space complexity Analysis: Given n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
                                    Input Space Complexity :
                                    - Space : O(n) -> timePreferences (list[list]) : A list of lists timePreferences of outer length n. For i ∈ 0, 1, . . . , n - 1, timePreferences[i] contains a permutation of the elements of set {0, 1, . . . , 19} to indicate the time slot preferences of student i. 
                                                        The time slots in timePreferences[i] appear in order of preference, with the time slot that student i likes the most appearing first.
                                    - Space : O(m) -> proposedClasses (list[list]) : A list of lists proposedClasses of outer length m. For j ∈ 0, 1, . . . , m - 1: proposedClasses[j][0] denotes the proposed time slot for the j-th class. Potentially, there can be multiple FIT2004 applied classes running in parallel.
                                                        proposedClasses[j][1] and proposedClasses[j][2] are positive integers that denote respectively, the minimum and maximum number of students that can be
                                                        allocated to the j-th class to satisfy the space occupancy constraints.
                
                                    Auxilary Space Complexity : 
                                    - Space : O(n+m+t) -> This function will first create the vertices/nodes for the all of the proposed class nodes, time slot nodes (which represent the time from 0-19, 20 nodes constant), student nodes, the source nodes, the sink nodes, and the super sink nodes.
                                    - Space : O(n*t) ->  It will then models the relationship of student time preferences and proposed class in a form of an edge from the class nodes to student nodes. 
                                                        The satisified student will have an edge from every time node where the class time is in that student top 5 time preferences list to the respective satisfied student nodes and also a reverse edge. 
                                                            The edge will have a flow of 0 and reverse edge will have a flow of 1, both will have a capacity of 1.
                                                        The non satisified student will have an edge from every time node where the class time is NOT in that student top 5 time preferences list to the respective non satisfied student nodes and also a reverse edge. 
                                                            The edge will have a flow of 0 and reverse edge will have a flow of 1, both will have a capacity of 1.
                                    - Space : O(t*m) ->  The time nodes will have an incoming edge from every class node where the class time is equal to that of the time nodes and also a reverse edge. 
                                                            The edge will have a flow of 0 and reverse edge will have a flow of (maximum capacity - minimum capacity) of that specific proposed class, both will have a capacity of the proposed class maximum capacity.
                                    - Space : O(m) ->  This function will then create an edge and reverse edge from the source nodes to every class nodes with a capacity of: residual capacity = maximum class capacity - minimum class capacity.
                                                        The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.
                                    - Space : O(1) ->  Next, it wll Check whether the number of student is less than the sum of all classes minimum capacity constraint or the number of student is greater than the sum of all classes maximum capacity constraint
                                                        This is a first layer check whether it is feasible to satisfy all constraints.
                                    - Space : O(1) ->It will then create an edge and reverse edge from super source/augmented source nodes to source nodes with a capacity of : the number of student - (total_sink_capacity = the sum of every minimum class capacity).
                                                        The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.
                                    - Space : O(n) ->  Lastly, it will create an edge and reverse edge from the all of the student nodes to the sink node with a capacity of 1.
                                                        The edge will have a flow of 0 and reverse edge will have a flow equal to the capacity.

                                    Therefore, the final Space complexity is : O(n + m + n+m + n*t + m*t + 1 + n) = O(n*t + m*t)
		
	"""

    # Add vertices for student, classess, sink, source, and augmented/super sink to the list
    # The structure of the adjacency list is : [m | time_slot | satisfied student nodes (n)| non satisfied student nodes (n) | source | sink | augmented/super source]
    # Time : O(m+t+n), Space : O(m+t+n), where n is the number of students to be allocated to FIT2004 applied classes and m is the number of proposed FIT2004 applied classes in the draft and t is the total number of time slot available.
    adjacency_list = []
    for _ in range((m+total_time_slot+2*n+2+1)):
        adjacency_list.append([])

    # Add forward edges and reverse edges from time node to satisfied student node that is in their top 5 time preferences list.
    # Time : O(n), Space : O(n), where n is the number of students to be allocated to FIT2004 applied classes.
    for stu_id, student in enumerate(timePreferences):
        stu_id += m+total_time_slot
        student = student[:5]
        for preference in student:
            for time, _ in enumerate(range(total_time_slot)):
                node_id = time+m
                if preference == time:
                    forward = Edge(stu_id, None, 1, 0)
                    backward = Edge(node_id, time, 1, 1)
                    forward.reverse = backward
                    backward.reverse = forward
                    adjacency_list[node_id].append(forward)
                    adjacency_list[stu_id].append(backward)

    # Add forward edges and reverse edges from time node to non satisfied student node that is NOT in their top 5 time preferences list.
    # and Add forward edges and reverse edges from non satisfied student node to the respective satisfied student node.
    # Time : O(n*t), Space : O(n*t), where n is the number of students to be allocated to FIT2004 applied classes and t is the total number of time slot available.
    for stu_id, student in enumerate(timePreferences):
        non_satisfied_stu_id = stu_id+m+total_time_slot+n
        stu_id += m+total_time_slot
        student = student[5:]
        for preference in student:
            for time, _ in enumerate(range(total_time_slot)):
                node_id = time+m
                if preference == time:
                    forward = Edge(non_satisfied_stu_id, None, 1, 0)
                    backward = Edge(node_id, time, 1, 1)
                    forward.reverse = backward
                    backward.reverse = forward
                    adjacency_list[node_id].append(forward)
                    adjacency_list[non_satisfied_stu_id].append(backward)

        # Add forward edges and reverse edges from non satisfied student node to the respective satisfied student node.
        forward = Edge(stu_id, None, 1, 0)
        backward = Edge(non_satisfied_stu_id, None, 1, 1)
        forward.reverse = backward
        backward.reverse = forward
        adjacency_list[non_satisfied_stu_id].append(forward)
        adjacency_list[stu_id].append(backward)

    # Add forward edges and reverse edges from class node to time node
    # Time : O(t*m), Space : O(t*m), where m is the number of proposed FIT2004 applied classes in the draft and t is the total number of time slot available.
    for time, _ in enumerate(range(total_time_slot)):
        augmented_source = len(adjacency_list)-1
        total_min_source_capacity = 0
        node_id = time+m
        for class_node_id, class_node in enumerate(proposedClasses):
            if time == class_node[0]:
                capacity = class_node[2]-class_node[1]
                total_min_source_capacity += class_node[1]
                forward = Edge(node_id, None, capacity, 0)
                backward = Edge(class_node_id, time, capacity, capacity)
                forward.reverse = backward
                backward.reverse = forward
                adjacency_list[class_node_id].append(forward)
                adjacency_list[node_id].append(backward)
    
        # Add forward edges and reverse edges from augment source to time nodes for the reduced demands
        # Time : O(1), Space : O(1)
        forward_augment = Edge(node_id, None, total_min_source_capacity, 0)
        backward_augment = Edge(augmented_source, None, total_min_source_capacity, total_min_source_capacity)
        forward_augment.reverse = backward_augment
        backward_augment.reverse = forward_augment
        adjacency_list[augmented_source].append(forward_augment)
        adjacency_list[node_id].append(backward_augment)

    # Add forward edges and reverse edges from source node to class nodes.
    # Time : O(m), Space : O(m), where m is the number of proposed FIT2004 applied classes in the draft.
    total_min_source_capacity = 0
    total_max_source_capacity = 0
    for node_index, class_node in enumerate(proposedClasses):

        # Add Add forward edges and reverse edges from source node to class nodes
        source = len(adjacency_list)-3
        capacity = class_node[2]-class_node[1]
        total_min_source_capacity += class_node[1]
        total_max_source_capacity += class_node[2]

        forward = Edge(node_index, None, capacity, 0)
        backward = Edge(source, None, capacity, capacity)
        forward.reverse = backward
        backward.reverse = forward
        adjacency_list[source].append(forward)
        adjacency_list[node_index].append(backward)


    # Check whether the number of student is less than the sum of all classes minimum capacity constraint or the number of student is greater than the sum of all classes maximum capacity constraint
    # This is a first layer check whether it is feasible to satisfy all constraints.
    # Time : O(1), Space : O(1)
    if n < total_min_source_capacity or n > total_max_source_capacity:
        return None
    
    # Add forward edges and reverse edges from augmented/super source to source node
    # Time : O(1), Space : O(1)
    source = len(adjacency_list)-3
    augmented_source = len(adjacency_list)-1
    forward = Edge(source, None, n-total_min_source_capacity, 0)
    backward = Edge(augmented_source, None, n-total_min_source_capacity, n-total_min_source_capacity)
    forward.reverse = backward
    backward.reverse = forward
    adjacency_list[augmented_source].append(forward)
    adjacency_list[source].append(backward)

    # Add forward edges and reverse edges from satisfied student nodes to sink node
    # Time : O(n), Space : O(n), where n is the number of students to be allocated to FIT2004 applied classes.
    for stu_id, student in enumerate(timePreferences):
        stu_id += m+total_time_slot
        sink = len(adjacency_list)-2

        forward = Edge(sink, None, 1, 0)
        backward = Edge(stu_id, None, 1, 1)
        forward.reverse = backward
        backward.reverse = forward
        adjacency_list[stu_id].append(forward)
        adjacency_list[sink].append(backward)



    return adjacency_list

def modified_ford_fulkerson(graph: list[list], s: int, t: int, n: int, m: int, total_time_slot: int, proposedClasses: list[list]) -> list[list]:
    """
		Function description: This function is use to recursively find an augmented path from the start nodes (source nodes) to the target nodes (super sink/augmented sink nodes) and update the flow of both the forward edges and backward edges using depth first search algorithm in the reduced augmented circular demand with lower bound network flow graph until it reaches its maxmum flow.
                                Primarly, this function is used to find the optimal flow network of the reduced augmented circular demand with lower bound network flow graph.

		Approach description: This function will first Initiate the max flow and augment value to 0. It will also Initialise the visited list into False for all the value.
                                Next, it will Find a path from the source to the target in the augmented reduced circular demand with lowerbound network flow graph and increase the flow of each edge with the bottleneck value in that path  until it reaches its maximum flow.
                                For each path found, it will Reset the visited list into all false.
                                The algorithm stops when there are no path from the source to the target in the augmented reduced circular demand with lowerbound network flow graph, denoted with the modified_dfs() returns 0.
                                Next, after the max-flow network is found, Add the minimum capacity of the clasess back to the forward edges from the class nodes to time nodes. 
                                Then, Add the minimum capacity of the clasess back to the forward edges from the source nodes to class nodes. 
                                
		Input: 
            graph (list[list]) : A list of list, an adjacency list, representing the reduced augmented circular demand with lower bound network flow graph.
			s (int) : A positive integer u denoting the source nodes/vertex
            t (int) : A positive integer t denoting the super sink/augmented sink/target nodes/vertex
            n (int) : A positive integer n denoting the number of students to be allocated to FIT2004 applied classes.
            m (int) : A positive integer m denoting the number of proposed FIT2004 applied classes in the draft.
            total_time_slot (int) : A positive integer t denoting the total number of time slot available.

            proposedClasses: lis[list] : A list of lists proposedClasses of outer length m. For j ∈ 0, 1, . . . , m - 1: proposedClasses[j][0] denotes the proposed time slot for the j-th class. Potentially, there can be multiple FIT2004 applied classes running in parallel.
                                            proposedClasses[j][1] and proposedClasses[j][2] are positive integers that denote respectively, the minimum and maximum number of students that can be
                                            allocated to the j-th class to satisfy the space occupancy constraints.

		Output: (list[list]) : returns a list of list, an adjacency list that represent the filled flow network of augmented reduced circular demand with lowerbound network flow graph to max flow,

        IMPORTANT : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!!! 
            For the following time and space complexity,
                This function is independent from the assingnment specification constraints, the time and space complexity is dependent on the input. Thus, the calculation of time and space complexity is not dependent on the assingnment specification constraints.
                The final time and space complexity considering the assingnment specification constraints will be calculated and explained in crowdedCampus() function.
        !!!!
        !!!!
            Every time and space complexity that is present in this function referes to their worst case time and space complexity.
        !!!!
		
		Time complexity: O(n*(n*t + m*t)), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.

		Time complexity analysis : Given n is the number of students to be allocated to FIT2004 applied classes and m is the number of proposed FIT2004 applied classes in the draft.
                                    - Time : O(1) -> Initiate the max flow and augment value
                                    - Time : O(n+m) -> Initialise the visited list into False for all the value
                                    - Time : O(n*(n*t + m*t)) -> Find a path from the source to the super sink/augmented sink/target in the augmented reduced circular demand with lowerbound network flow graph 
                                                            and increase/update the flow of both the forward edges and backward edges with the bottleneck value in that path until it reaches its maximum flow.
                                                            Whereas the maximum flow is at worst/upper bound is equal to the number of student.
                                    - Time : O(m*t) -> Add the minimum capacity of the clasess back to the forward edges from the class nodes to time nodes. 

                                    Therefore, the final time complexity is : Time : O(n*(n*t + m*t))

		Space complexity: O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.

        Space complexity Analysis: Given n is the number of students to be allocated to FIT2004 applied classes and m is the number of proposed FIT2004 applied classes in the draft.
                                    The space complexity of this function depends on the input and also the visited list, the upperbound of the input is the adjacency list that represent the reduced augmented circular demand with lowerbound network flow graph, which has O(n*m) space complexity.
                                    Proven below : 

                                    Input Space :
                                    - Space : O(n*t + m*t) -> graph (list[list]) : A list of list, an adjacency list, representing the reduced augmented circular demand with lower bound network flow graph.
                                    - Space : O(1) -> s (int) : A positive integer u denoting the start nodes/vertex
                                    - Space : O(1) -> t (int) : A positive integer t denoting the target nodes/vertex
                                    - Space : O(1) -> n (int) : A positive integer n denoting the number of students to be allocated to FIT2004 applied classes.
                                    - Space : O(1) -> m (int) : A positive integer m denoting the number of proposed FIT2004 applied classes in the draft.
                                    - Space : O(m) -> proposedClasses: lis[list] : A list of lists proposedClasses of outer length m. For j ∈ 0, 1, . . . , m - 1: proposedClasses[j][0] denotes the proposed time slot for the j-th class. Potentially, there can be multiple FIT2004 applied classes running in parallel.
                                                        proposedClasses[j][1] and proposedClasses[j][2] are positive integers that denote respectively, the minimum and maximum number of students that can be
                                                        allocated to the j-th class to satisfy the space occupancy constraints.

                                    Auxilary Space : 
                                    - Space : O(n+m+t) -> visited (list) : A list of nodes, denoting whether a nodes has been visited or not.
                                    - Space : O(t*n + t*m) -> The time list that contain all time nodes
                                    - Space : O(t*n + t*m) -> Add the minimum capacity of the clasess back to the forward edges from the class nodes to time nodes. 
                                    Therefore, the final upperbound space complexity is : Space : O(n*t + m*t)       
		
	"""

    # Initiate the max flow and augment value
    # Time : O(1), Space O(1)
    max_flow = 0
    augment = math.inf

    # Initialise the visited list into False for all the nodes/vertices in the graph
    # Time : O(n+m+t), Space O(n+m+t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    visited = []
    for _ in range((2*n+m+total_time_slot+2+1)):
        visited.append(False)

    # Find a path from the source to the super sink/augmented sink/target in the augmented reduced circular demand with lowerbound network flow graph 
    # and increase/update the flow of both the forward edges and backward edges with the bottleneck value in that path until it reaches its maximum flow.
    # Time : O(n*(n*t + m*t)), Space : O(1), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    while augment > 0:

        # Reset the visited list into all false
        # Time : O(n+m+t), Space O(1), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
        for index, _ in enumerate(visited):
            visited[index] = False

        # Find a bottleneck value in the path from the source to the super sink/augmented sink/target in the augmented reduced circular demand with lowerbound network flow graph
        # and increase/update the flow of both the forward edges and backward edges with the bottleneck value in that path.
        augment = modified_dfs(s, t, math.inf, visited, graph)
        max_flow += augment

    # Add the minimum capacity of the clasess back to the forward edges from the class nodes to time nodes. 
    # This, represent the combination of the lower bound graph with the filled residual network flow graph.
    # Time : O(m*t), Space : O(t*m+t*n), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    time_list = graph[m:m+total_time_slot]
    for class_index, class_nodes in enumerate(proposedClasses):
        for edges in time_list:
            for edge in edges:
                if edge.to == class_index:
                    edge.reverse.flow += class_nodes[1]

    # Add the minimum capacity of the clasess back to the forward edges from the source nodes to class nodes. 
    # This, represent the combination of the lower bound graph with the filled residual network flow graph.
    # Time : O(m), Space : O(1), where m is the number of proposed FIT2004 applied classes in the draft.
    # the source nodes is in the length of the graph -3
    for edge in graph[-3]:
        for class_index, class_nodes in enumerate(proposedClasses):
                
            if edge.to == class_index:
                edge.flow += class_nodes[1]

    return graph

def modified_dfs(u: int, t: int, bottleneck: int, visited: list[list], graph: list[list[Edge]]) -> int:
    """
		Function description: This function is use to recursively find the bottleneck in the augmented path from the start nodes (source nodes) to the target nodes (super sink/augmented sink nodes) and update the flow of both the forward edges and backward edges using depth first search algorithm in the reduced augmented circular demand with lower bound network flow graph.

		Approach description: This function is use to to recursively find the bottleneck in the augmented path from the start nodes (source nodes) to the target nodes (super sink/augmented sink nodes) and update the flow of both the forward edges and backward edges using depth first search (DFS) algorithm in the reduced augmented circular demand with lower bound network flow graph.
                                The base case of this DFS function algorithm is when the algorithm reaches the super sink/augmented sink/target nodes. 
                                When the algorithm hit its base case, it return the smallest edge capacity that it found in the path from the source nodes to the base case (super sink/augmented sink/target nodes), the smallest edge capacity in the path is called the bottleneck.
                                Furthermore, once the algorithm hit its base case, it will backtrack the path and increase the flow of the edges in that path by the bottleneck value.
                                If the algorithm  hasn't reach the base case, it will do DFS search to find the super sink/augmented sink/target nodes, while updating the bottleneck whenever it finds a smaller edge capacity.
                                
		Input: 
			u (int) : A positive integer u denoting the start nodes/vertex
            t (int) : A positive integer t denoting the target nodes/vertex

            bottleneck (int) : A positive integer denoting the current bottleneck value, the bottleneck value is the smallest edge capacity in the path towards the target nodes.
                
            visited (list) : A list of nodes, denoting whether a nodes has been visited or not.

            graph (list[list]) : A list of list, an adjacency list, representing the reduced augmented circular demand with lower bound network flow graph.

		Output: (int) : returns an augmented flow/the bottleneck value of each augmented path found, an augmented path is a path from the source nodes to the super sink/augmented sink/target nodes in the reduced augmented circular demand with lower bound network flow graph.

        IMPORTANT : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!!! 
            For the following time and space complexity,
                This function is independent from the assingnment specification constraints, the time and space complexity is dependent on the input. Thus, the calculation of time and space complexity is not dependent on the assingnment specification constraints.
                The final time and space complexity considering the assingnment specification constraints will be calculated and explained in crowdedCampus() function.
        !!!!
        !!!!
            Every time and space complexity that is present in this function referes to their worst case time and space complexity.
        !!!!
		
		Time complexity: O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.

		Time complexity analysis : Given n is the number of students to be allocated to FIT2004 applied classes and m is the number of proposed FIT2004 applied classes in the draft.
                                    - Time : O(n*t + m*t) -> The worst case scenario of the DFS algorithm is that it will visit every node and every edges in the pursuit of the super sink/augmented sink/target nodes.
                                                                Additionally, the worst case scenario would be that the reduced augmented circular demand with lower bound network flow graph is a dense graph.
                                                                In a directed graph, the upper bound of edges we can have is the squared of the number of vertices/nodes in the graph, hence a dense graph.
                                                                Therefore the worst case time complexity of this function is equal to that of the the number of edges in the reduced augmented circular demand with lowerbound network flow graph, which is O(n+m).
                                
                                    Therefore, the final time complexity is : Time : O(n*t + m*t)

		Space complexity: O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.

        Space complexity Analysis: Given n is the number of students to be allocated to FIT2004 applied classes and m is the number of proposed FIT2004 applied classes in the draft.
                                    The space complexity of this function entirely depends on the input, the upperbound of the input is the adjacency list that represent the reduced augmented circular demand with lowerbound network flow graph, which has O(n*m) space complexity.
                                    Proven below : 

                                    - Space : O(1) -> u (int) : A positive integer u denoting the start nodes/vertex
                                    - Space : O(1) -> t (int) : A positive integer t denoting the target nodes/vertex
                                    - Space : O(1) -> bottleneck (int) : A positive integer denoting the current bottleneck value, the bottleneck value is the smallest edge capacity in the path towards the target nodes.
                                    - Space : O(n+m+t) -> visited (list) : A list of nodes, denoting whether a nodes has been visited or not.
                                    - Space : O(n*t + m*t) -> graph (list[list]) : A list of list, an adjacency list, representing the reduced augmented circular demand with lower bound network flow graph.

                                    Therefore, the final space complexity is : Space : O(n*t + m*t)       
		
	"""

    # Base case is when it reaches the super sink/augment sink/target nodes
    # Time : O(1), Space : O(1)
    if u == t:
        return bottleneck

    # Find a path from the source to the sink/target in the reduced augmented circular demand with lowerbound network flow graph using DFS.
    # Worst case scenario is that it visits every nodes and edges in the graph.
    # Time : O(n*t + m*t), Space : O(1), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    visited[u] = True
    for edge in graph[u]:
        residual = edge.capacity - edge.flow
        if residual > 0 and not visited[edge.to]:
            augment = modified_dfs(edge.to, t, min(bottleneck, residual), visited, graph)
            if augment > 0 :
                edge.flow += augment
                edge.reverse.flow -= augment
                return augment
                
    return 0

def student_allocation(total_time_slot: int, timePreferences: list[list], proposedClasses: list[list], minimumSatisfaction: int, graph: list[list]) -> list|None:
    """
		Function description: This function is used to determine the validity of the proposedClassess, whether or not there is a valid student allocation that satisfy all constraints, which are : 
                                • Each student is allocated to exactly one class.
                                • Each proposed class satisfies its space occupancy constraints.
                                • At least minimumSatisfaction students get allocated to classes with class times that are
                                    within their top 5 preferred time slots.
                                If it does meet all constraints, then it will note/record all of the student that have been allocated to a class into the student allocated list, including which class they are allocated to.
                                This function uses the filled network flow graph to determine which student is allocated to which class.

		Approach description: The function will firstly, Define the start and end student id in the reduced augmented circular demand with lowerbound network flow graph and define the students list that contain all of the student id and all of the outgoing edges.
                                Next, it will Initialise the student allocated list, to contain all of the allocated student and Initialise the number of student who is satisfied with their allocated class time.
                                The function will iterate all outgoing edges except the the edges to the sink nodes from the student nodes in the filled reduced augmented circular demand with lower bound network flow graph.
                                In each iteration it will record the class time allocation of the student based on the outgoing edges to the time nodes from the student nodes, which have a flow of 0.
                                It will also check whether the allocated class time of the student falls within the top 5 of the student's time preferences, using the minimum_sats variable.
                                Next, it will List all of the outgoing edges, their time slot, and their flow from the time nodes in the class list.
                                Then, Iteratively assigned student that is allocated to a particular class time to the the class number, that have the same class time, using the filled edges from the time nodes to the class nodes as its capacity.
                                It will then check whether it meets all of the constraints, which are : 
                                • Each student is allocated to exactly one class.
                                • Each proposed class satisfies its space occupancy constraints.
                                • At least minimumSatisfaction students get allocated to classes with class times that are
                                    within their top 5 preferred time slots.                                
                                
		Input: 
            total_time_slot (int) : A positive integer t denoting the total number of time slot available.

            timePreferences (list[list]) : A list of lists timePreferences of outer length n. For i ∈ 0, 1, . . . , n - 1, timePreferences[i] contains a permutation of the elements of set {0, 1, . . . , 19} to indicate the time slot preferences of student i. 
                                            The time slots in timePreferences[i] appear in order of preference, with the time slot that student i likes the most appearing first.

            proposedClasses (list[list]) : A list of lists proposedClasses of outer length m. For j ∈ 0, 1, . . . , m - 1: proposedClasses[j][0] denotes the proposed time slot for the j-th class. Potentially, there can be multiple FIT2004 applied classes running in parallel.
                                            proposedClasses[j][1] and proposedClasses[j][2] are positive integers that denote respectively, the minimum and maximum number of students that can be
                                            allocated to the j-th class to satisfy the space occupancy constraints.
                
            minimumSatisfaction (int) : A positive integer minimumSatisfaction. It holds that minimumSatisfaction ≤ n.


            graph (list[list]) : A list of list, an adjacency list, representing the filled reduced augmented circular demand with lower bound network flow graph.

		Output: (list|None) : returns a list of all student along with their allocated class.
                        
        IMPORTANT : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!!! 
            For the following time and space complexity,
                This function is independent from the assingnment specification constraints, the time and space complexity is dependent on the input. Thus, the calculation of time and space complexity is not dependent on the assingnment specification constraints.
                The final time and space complexity considering the assingnment specification constraints will be calculated and explained in crowdedCampus() function.
        !!!!
        !!!!
            Every time and space complexity that is present in this function referes to their worst case time and space complexity.
        !!!!
		
		Time complexity: O(m*t*n), where n is the number of students to be allocated to FIT2004 applied classes and m is the number of proposed FIT2004 applied classes in the draft.

		Time complexity analysis : Given n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
                                   The upper bound time complexity of this function is :
                                    Time : O(n) -> The function will firstly, Define the start and end student id in the reduced augmented circular demand with lowerbound network flow graph and define the students list that contain all of the student id and all of the outgoing edges.
                                    Time : O(n*t) -> Next, it will Initialise the student allocated list, to contain all of the allocated student and Initialise the number of student who is satisfied with their allocated class time.
                                                        The function will iterate all outgoing edges except the the edges to the sink nodes from the student nodes in the filled reduced augmented circular demand with lower bound network flow graph.
                                                        In each iteration it will record the class time allocation of the student based on the outgoing edges to the time nodes from the student nodes, which have a flow of 0.
                                                        It will also check whether the allocated class time of the student falls within the top 5 of the student's time preferences, using the minimum_sats variable.
                                    Time : O(t*m + t*n) -> Next, it will List all of the outgoing edges, their time slot, and their flow from the time nodes in the class list.
                                    Time : O(m*t*n) -> Then, Iteratively assigned student that is allocated to a particular class time to the the class number, that have the same class time, using the filled edges from the time nodes to the class nodes as its capacity.
                                    Time : O(1) -> It will then check whether it meets all of the constraints, which are : 
                                                    • Each student is allocated to exactly one class.
                                                    • At least minimumSatisfaction students get allocated to classes with class times that are
                                                        within their top 5 preferred time slots.         

                                    Therefore, the final time complexity is : Time : O(m*t*n)

		Space complexity: O(n*t + m*t), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
        Space complexity Analysis: Given n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
                                   The upper bound space complexity of this function is :

                                   Input Space :
                                    - Space : O(n) -> timePreferences (list[list]) : A list of lists timePreferences of outer length n. For i ∈ 0, 1, . . . , n - 1, timePreferences[i] contains a permutation of the elements of set {0, 1, . . . , 19} to indicate the time slot preferences of student i. 
                                                        The time slots in timePreferences[i] appear in order of preference, with the time slot that student i likes the most appearing first.
                                    - Space : O(m) -> proposedClasses (list[list]) : A list of lists proposedClasses of outer length m. For j ∈ 0, 1, . . . , m - 1: proposedClasses[j][0] denotes the proposed time slot for the j-th class. Potentially, there can be multiple FIT2004 applied classes running in parallel.
                                                        proposedClasses[j][1] and proposedClasses[j][2] are positive integers that denote respectively, the minimum and maximum number of students that can be
                                                        allocated to the j-th class to satisfy the space occupancy constraints.
                                    - Space : O(n*t + m*t) -> graph (list[list]) : A list of list, an adjacency list, representing the reduced augmented circular demand with lower bound network flow graph.

                                   Auxilary Space :
                                    - Space : O(n*t) -> The function will firstly, Define the start and end student id in the reduced augmented circular demand with lowerbound network flow graph and define the students list that contain all of the student id and all of the outgoing edges.
                                    - Space : O(n) -> Next, it will Initialise the student allocated list, to contain all of the allocated student and Initialise the number of student who is satisfied with their allocated class time.
                                                        The function will iterate all outgoing edges except the the edges to the sink nodes from the student nodes in the filled reduced augmented circular demand with lower bound network flow graph.
                                                        In each iteration it will record the class time allocation of the student based on the outgoing edges to the time nodes from the student nodes, which have a flow of 0.
                                                        It will also check whether the allocated class time of the student falls within the top 5 of the student's time preferences, using the minimum_sats variable.
                                    - Space : O(t*m) -> Next, it will List all of the outgoing edges, their time slot, and their flow from the time nodes in the class list.
                                    - Space : O(1) -> Then, Iteratively assigned student that is allocated to a particular class time to the the class number, that have the same class time, using the filled edges from the time nodes to the class nodes as its capacity.
                                    - Space : O(1) -> It will then check whether it meets all of the constraints, which are : 
                                                    • Each student is allocated to exactly one class.
                                                    • At least minimumSatisfaction students get allocated to classes with class times that are
                                                        within their top 5 preferred time slots.   

                             

                                    Therefore, the final space complexity is : Space : O(n*t + m*t)      
		
	"""   

    # Define the start and end student id in the reduced augmented circular demand with lowerbound network flow graph
    # And define the students list that contain all of the student id and all of the outgoing edges.
    # Time : O(n), Space : O(n*t), where n is the number of students to be allocated to FIT2004 applied classes and t is the total number of time slot available.
    stu_id_begin_nodes = total_time_slot+len(proposedClasses)
    stu_id_end_nodes = 2*len(timePreferences) + total_time_slot + len(proposedClasses)
    students = graph[stu_id_begin_nodes:stu_id_end_nodes]

    # Initialise the student allocated list, to contain all of the allocated student.
    # Time : O(1), Space : O(1)
    student_allocated = []
    for _ in range(len(timePreferences)):
        student_allocated.append(None)
    # Initialise the number of student who is satisfy of their allocated class time.
    # Time : O(1), Space : O(1)
    minimum_sats = 0

    # Note all of the student that have been allocated to a class time into the student allocated list, including which class time they are allocated to 
    # and check whether the allocated class time of the student falls within the top 5 of the student's time preferences, using the minimum_sats variable.
    # Time : O(n*t), Space : O(n), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    for stu_id, edges in enumerate(students):
        stu_id = stu_id%len(timePreferences)
        for edge in edges:
            for time in range(total_time_slot):
                time_id = time+len(proposedClasses)

                if edge.to == time_id:
                    if edge.flow == 0:
                        student_allocated[stu_id] = edge.to

                        if edge.time_slot in timePreferences[stu_id][:5]:
                            minimum_sats += 1


                    
   
    # List all of the outgoing edges, their time slot, and their flow from the time nodes.
    # Time : O(t*m + t*n), Space : O(t*m), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    class_list = []
    for time_nodes in range(total_time_slot):
        time_id = time_nodes+len(proposedClasses)
        for edge in graph[time_id]:
            # Continue if the nodes are not class nodes.
            if edge.time_slot != None :
                class_list.append((edge.to, edge.time_slot, edge.reverse.flow))

    # Iteratively assigned student that is allocated to a particular class time to the the class number, that have the same class time,
    # using the filled edges from the time nodes to the class nodes as its capacity.
    # Time : O(m*t*n), Space : O(1), where n is the number of students to be allocated to FIT2004 applied classes, m is the number of proposed FIT2004 applied classes in the draft, and t is the total number of time slot available.
    for class_nodes in class_list:
        class_occupancy = 0
        
        for stu_id, time_nodes in enumerate(student_allocated):
            time_nodes -= len(proposedClasses)

            if class_nodes[1] == time_nodes:
                if class_occupancy >= class_nodes[2]:
                    break
  
                student_allocated[stu_id] = class_nodes[0]
                class_occupancy += 1
            
    
    # Check whether the number of student who is satisfied with their allocated class, satisfy the minimumSatisfaction constraints and whether all student is allocated to a class.
    # Time : O(1), Space : O(1)
    if minimum_sats < minimumSatisfaction or len(student_allocated) != len(timePreferences):
        return None

    return student_allocated

########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# QUESTION 2 #

class Node:
    """
		Class description: This class is used to define a Node as an object with the following attribute:
                            self.node_list = A list with a length of 27, where the index represent the alphabetical order, and is used to store the pointer to the corresponding alphabet node.

    """
    def __init__(self) -> None:
        """
            Function description: This function initialise and defines the following attribute : 
                                    self.node_list = A list with a length of 27, where the index represent the alphabetical order, and is used to store the pointer to the corresponding alphabet node.
                    
            Input: None
                
            Output: None
                
            Time complexity: O(1)

            Time complexity analysis :  Because this class only create a list with a length of 27

            Space complexity: O(1)

            Space complexity analysis:  Because this class only create a list with a length of 27
        """

        # Initialise all of the cells as None
        self.node_list = []
        for _ in range(27):
            self.node_list.append(None)

class Trie:
    """
		Class description: This class is used to define a Node as an object with the following attribute:
                            self.root = A root node
     
    """
    def __init__(self) -> None:
        """
            Function description: This function initialise and defines the following attribute : 
                                    self.root = A root node
                    
            Input: None
                
            Output: None
                
            Time complexity: O(1)

            Time complexity analysis : Because this class only assign a constant length list to a variable

            Space complexity: O(1)

            Space complexity analysis: Because this class only assign a constant length list to a variable
        """
        # Initialise the root node of the trie
        self.root = Node()

    def insert(self, word: list) -> None:
        """
            Function description: This function is used to insert a word into the prefix trie.
            
            Approach Description: This function will iterate every character of the word and recursively add that particular character index a pointer to the next node.

            Input: 
                word (list) : A list of characters (string) in a word
                
            Output: None
                
            Time complexity: O(M), Where M is the length of the longest word (upperbound)

            Time complexity analysis : This function will iterate every character of the word and recursively add that particular character index a pointer to the next node. T
                                        The Iteration and recursion happen at the same time, therefore, it will be dependent on the length of the word, which is O(M)

            Space complexity: O(M),  Where M is the length of the longest word (upperbound)

            Space complexity analysis: This function only insert/change a value inside of the trie, therefore it does not create a new space.
                                        Thus it only depends on the input space : 

                                        Space O(M) -> word (list) : A list of characters (string) in a word

                                        Therefore, the upperbound space complexity is : O(M)
        """

        # iterate every character of the word and recursively add that particular character index a pointer to the next node, 
        # at the end of the word, it will add a terminating character : '$'
        # Time : O(M), Space : O(1),  Where M is the length of the longest word (upperbound)
        node = self.root
        for char in word:
            if char == '$' and node.node_list[-1] == None:
                node.node_list[-1] = '$'
                break
            index = ord(char) - ord('a')
            if node.node_list[index] == None:
                node.node_list[index] = Node()
            node = node.node_list[index]

class Bad_AI:
    """
		Class description: This class is an object mainly used to identify words that have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
                            It has three functions which are : 
                            _init_() : is used to initialise the object Bad_AI Attribute value, which is to fill the trie with all of the words.
                            check_word() : is used to check whether the words have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
                            dfs_word_extraction() : is an auxilary function that is used to recursively iterate all words in the trie and identify words that have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
     
    """
    def __init__(self, list_words: list[list]) -> None:
        """
            Function description: This function is used to populate the trie with the words in the list_words using insert().
            
            Approach Description: This function will iterate every character of the words and recursively add that particular character to the trie using insert().

            Input: 
                lis_words (list[list]) : A list of words
                
            Output: None
                
            Time complexity: O(M*N) or O(C), Where M is the length of the longest word (upperbound), N is the number of words, and C is the number of characters in list_words

            Time complexity analysis : Given M is the length of the longest word (upperbound), N is the number of words, and C is the number of characters in list_words
                                        This function will iterate every character of the word for all words in the list_words and recursively add that particular character to the trie.
                                        The Iteration and recursion happen at the same time, therefore, it will be dependent on the length of the word times the number of words, which is O(M*N)

            Auxilary Space complexity: O(M*N) or O(C), Where M is the length of the longest word (upperbound), N is the number of words, and C is the number of characters in list_words

            Auxilary Space complexity analysis: Given M is the length of the longest word (upperbound), N is the number of words, and C is the number of characters in list_words
                                                This function only insert/change a value inside of the trie:
                    
                                                Auxilary Space : 
                                                    - Space O(M*N) or O(C) -> This function is used to populate the trie with the words in the list_words using insert(). 
                                                                        Each word will be inserted using insert() which has space complexity of O(M), and the number of words is N.
                                                
                                                Therefore, the upperbound worst-case auxilary space complexity is : O(C)
                                                    
        """
        # Populate the trie with the words in the list_words using insert().
        # Time :  O(M*N) or O(C), Space : O(M*N) or O(C), Where M is the length of the longest word (upperbound), N is the number of words, and C is the number of characters in list_words
        self.trie = Trie()
        for word in list_words:
            self.trie.insert(word+'$')

    def check_word(self, sus_word: list) -> list[list]:
        """
            Function description: This function is used to identify words that have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
            
            Approach Description: This function will iterate every character of the sus_word, while recursively iterate every characters in the trie and comparing it with the character of the sus_words using
                                    dfs_word_extraction() function. It will count the number of mismatch characters in the every word iterated. The dfs_word_extraction() function will then return
                                    the words that have exactly one from what they should be when only substitutions are considered. The output of dfs_word_extraction()  will be return in this function.

            Input: 
                sus_word (list) : A list of characters (word)
                
            Output: list[list] : a list of words.
                
            Time complexity:  O(J*N) + O(X), Where J is the length of the sus_word, N is the number of words in the trie, and X is the number of characters returned in the correct list.

            Time complexity analysis : Given J is the length of the sus_word, N is the number of words in the trie, and X is the number of characters returned in the correct list.
                                        - Time : O(J*N) + O(X) -> This function will use the dfs_word_extraction() to iterate every character of the sus_word, while recursively iterate every characters in the trie and comparing it with the character of the sus_words. 
                                                                    It will count the number of mismatch characters in every word iterated. The maximum recursion depth of recursively going through the trie would be equal to the length of the sus_word.
                                        
                                        Therefore the time complexity is dependent on the dfs_word_extraction() function, which is O(J*N) + O(X)

            Auxilary Space complexity: O(X), Where X is the number of characters returned in the correct list.

            Auxilary Space complexity analysis: Given X is the number of characters returned in the correct list and J is the length of the sus_word.
                                        Auxilary Space : 
                                            - Space : O(X) -> This function only run the dfs_word_extraction() function which has a space complexity of : O(X)

                                        Therefore, the upperbound space complexity of this function is O(X).
        """
        result = []
        depth_counter = 0
        mistakes = 0

        # This function is used as an auxilary function to recusrively identify words that have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
        # Time : O(J*N) + O(X), Space : O(X), Where J is the length of the sus_word, N is the number of words in the trie, and X is the number of characters returned in the correct list.
        self.dfs_word_extraction(self.trie.root, "", depth_counter, sus_word, mistakes, result)  

        return result

    def dfs_word_extraction(self, node: Node, word_path: list, depth_counter: int, sus_word: list, mistakes: int, result: list[list]) -> list[list]:
        """
            Function description: This function is used as an auxilary function to recusrively identify words that have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
            
            Approach Description: This function will iterate every character of the sus_word, while recursively iterate every characters in the trie and comparing it with the character of the sus_words. 
                                    It will count the number of mismatch characters in every word iterated. The maximum recursion depth of recursively going through the trie would be equal to the length of the sus_word.

            Input: 
                node (Node)         : A Node object
                word_path (list)    : A list of characters (word)
                depth_counter (int) : A positive integer indicating the trie depth (recursion depth)
                sus_word (list)     : A list of characters (word) of the suspicious word
                mistakes (int)      : A positive integer indicating the number of mismatches of characters between the iterated words with the sus_word
                result (list[list]) : A list of words that have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
                
            Output: list[list] : A list of words that have Levenshtein distance exactly one from what they should be when only substitutions are considered. 
                
            Time complexity:  O(J*N) + O(X), Where J is the length of the sus_word, N is the number of words in the trie, and X is the number of characters returned in the correct list.

            Time complexity analysis : Given J is the length of the sus_word, N is the number of words in the trie, and X is the number of characters returned in the correct list.
                                        - Time : O(J*N) -> This function will iterate every character of the sus_word, while recursively iterate every characters in the trie and comparing it with the character of the sus_words. 
                                                            It will count the number of mismatch characters in every word iterated. The maximum recursion depth of recursively going through the trie would be equal to the length of the sus_word.
                                                            Therefore the amount of character compared and extracted in this function would not be greater than the number of characters in the sus_word for every word iteration.

                                        - Time : O(X) -> After the recursion reach the sus_word length, and the mistake is equal to 1, and also the iterated word is also reach its end. It will Append that word to the result list.
                                                            Appending the string of all of the words that have Levenshtein distance exactly one from what they should be when only substitutions are considered, has a time complexity of 
                                                            O(X), Where X is the number of characters returned in the correct result list.

                                        Therefore the final time complexity is : O(J*N) + O(X)

            Space complexity: O(X), Where X is the number of characters returned in the correct list.

            Space complexity analysis: Given X is the number of characters returned in the correct list and J is the length of the sus_word.
                                        Input Space :
                                            - Space : O(1) -> node (Node) : A Node object
                                            - Space : O(J) -> word_path (list) : A list of characters, this list length would be <= to length of sus_word
                                            - Space : O(1) -> depth_counter (int) : A positive integer indicating the trie depth (recursion depth)
                                            - Space : O(J) -> sus_word (list) : A list of characters (word) of the suspicious word
                                            - Space : O(1) -> mistakes (int) : A positive integer indicating the number of mismatches of characters between the iterated words with the sus_word
                                            - Space : O(X) -> result (list[list]) : A list of words that have Levenshtein distance exactly one from what they should be when only substitutions are considered.

                                        Auxilary Space : 
                                            - Space : O(X) -> Creating the space for the result (list[list]) : A list of words that have Levenshtein distance exactly one from what they should be when only substitutions are considered.

                                        Therefore, the upperbound space complexity of this function is O(X), because O(X) has an upperbound greater than O(J), as X can consists of multiple words that have length equal to J
        """      
        
        if mistakes>1:
            return None

        # Check whether the recursive depth reached the length of the sus_word, and append the constructed word if there is only 1 mistake.
        # Time : O(word_path), Space : O(word_path)
        if depth_counter == len(sus_word):
            if node.node_list[-1] == '$' and mistakes == 1:
                result.append(word_path)
            return None
        
        # Recursively go through all nodes in an order and record the "mistakes", which are a characters that differs with the sus_word
        # Time : O(J*N) + O(X), Space : O(X), Where J is the length of the sus_word, N is the number of words in the trie, and X is the number of characters returned in the correct list.
        for i in range(26):
            child = node.node_list[i]

            if child:
                char = chr(i + ord('a'))
                if char == sus_word[depth_counter]:
                    self.dfs_word_extraction(child, word_path + char, depth_counter+1, sus_word, mistakes, result)
                else:

                    self.dfs_word_extraction(child, word_path + char, depth_counter+1, sus_word, mistakes+1, result)

n = 6
m = 6
timePreferences = [[0,1,2,3,4,5], [0,1,2,3,4,5], [0,1,2,3,4,5], [0,1,2,3,4,5], [0,1,2,3,4,5], [0,5,1,2,3,4]]
proposedClassess = [[0,1,1],[1,1,1],[2,1,1],[3,1,1],[4,1,1],[5,1,1]]

minimum_sats = 6

result = crowdedCampus(n,m,timePreferences,proposedClassess,minimum_sats)
print(result)