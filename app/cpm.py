from asyncio import tasks
import pandas as pd
import datetime

from criticalpath import Node
from datetime import date
import os

def add_nodes(tasks,key,value):
    item=(key,{"Duration":value})
    # item[key]={"Duration":value}
    tasks.append(item)
    return tasks

# tasks=[]
# add_nodes(tasks,"A",3)
# add_nodes(tasks,"B",5)
# add_nodes(tasks,"C",2)
# add_nodes(tasks,"D",3)
# add_nodes(tasks,"E",5)

# set up the dependencies along all paths:
# dependencies = [("A", "C"), 
#                 ("B", "C"), 
#                 ("A", "D"),
#                 ("C", "E"), 
#                 ("D", "E")]


def add_edges(dependencies,edge1,edge2):
    item=(edge1,edge2)
    dependencies.append(item)
    return dependencies

# dependencies=[]
# add_edges(dependencies,"A","B")
# add_edges(dependencies,"A","C")
# add_edges(dependencies,"B","D")
# add_edges(dependencies,"C","E")
# add_edges(dependencies,"D","E")


def critical_path(crit_path,dependencies,tasks):

    # initialize a "project":
    proj = Node('Project')

    # load the tasks and their durations:
    for t in tasks:
        proj.add(Node(t[0], duration=t[1]["Duration"]))

    # load the dependencies (or sequence):
    for d in dependencies:
        proj.link(d[0],d[1])

    # update the "project":
    proj.update_all()

    # proj.get_critical_path() will return a list of nodes
    # however, we want to store them as strings so that they can be easily used for visualization later
    crit_path = [str(n) for n in proj.get_critical_path()]

    # get the current duration of the project
    proj_duration = proj.duration

    print(f"The current critical path is: {crit_path}")
    print(">"*50)
    print(f"The current project duration is: {proj_duration} days")

    # create a list of edges using the current critical path list:
    crit_edges = [(n, crit_path[i+1]) for i, n in enumerate(crit_path[:-1])]
    return [crit_path,proj_duration]

#GANTT-CHART
def gc(dependencies,crit_path):
    proj_startdate = date.today()
    print("Proj start date",proj_startdate)
    proj_schedule = pd.DataFrame([dict(Task = key, 
                                    Start = datetime.date.today(), 
                                    Finish = datetime.date.today() + datetime.timedelta(val['Duration']), 
                                    Status = 'NA')
                                for key, val in dict(tasks).items()])

    for key, val in dict(tasks).items():
        dep = [d for d in dependencies if d[1] == key]
        prev_tasks = [t[0] for t in dep]
        if prev_tasks:
            prev_finish = proj_schedule[proj_schedule.Task.isin(prev_tasks)]['Finish'].max()
            proj_schedule.loc[proj_schedule.Task == key, 'Start'] = prev_finish
            proj_schedule.loc[proj_schedule.Task == key, 'Finish'] = prev_finish + datetime.timedelta(val['Duration'])
            
    proj_schedule.loc[proj_schedule.Task.isin(crit_path), 'Status'] = 'Critical Path'
            
    display(proj_schedule)
# crit_path=[]
# critical_path(crit_path,dependencies,tasks)
# gc(dependencies,crit_path)