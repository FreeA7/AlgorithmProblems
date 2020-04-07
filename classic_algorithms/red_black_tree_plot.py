# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 12:36:37 2020

@author: FreeA7

Plot and save image of red black tree
"""

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

class RedBlackTreePloter(object):
    @staticmethod
    def __getNodeInfos(redblacktree):
        infos = {'coordinates':{}}
        index = 1
        deepest = 0
        for node in redblacktree.inorderNode():
            depth = deepest = 1
            parent = node
            while parent.parent:
                parent = parent.parent
                depth += 1
            infos['coordinates'][node.value] = [index, depth, node.color]
            if deepest < depth: deepest = depth
            index += 1
        for value in infos['coordinates'].keys():
            infos['coordinates'][value] = (infos['coordinates'][value][0], deepest+1-infos['coordinates'][value][1], infos['coordinates'][value][2])
        infos['width'] = index
        infos['height'] = deepest
        return infos
    
    @staticmethod
    def __getLineCoordinate(redblacktree, node_infos):
        lines = []
        for node in redblacktree.inorderNode():
            if node.parent:
                lines.append(((node_infos['coordinates'][node.value][0], node_infos['coordinates'][node.parent.value][0]), 
                              (node_infos['coordinates'][node.value][1], node_infos['coordinates'][node.parent.value][1])))
        return lines
    
    @staticmethod
    def __plotCircle(infos, ax):
        fontsize = 200//max(infos['width'], infos['height'])
        
        for value in infos['coordinates'].keys():
            if infos['coordinates'][value][2]:
                circle = mpatches.Circle((infos['coordinates'][value][0], infos['coordinates'][value][1]), 0.5, color='red')
                
            else:
                circle = mpatches.Circle((infos['coordinates'][value][0], infos['coordinates'][value][1]), 0.5, color='grey')
            circle.set_zorder(1)
            ax.add_patch(circle)
            if value == None:
                plt.text(infos['coordinates'][value][0], infos['coordinates'][value][1], 'N', fontsize=fontsize, verticalalignment='center', horizontalalignment='center')    
            else:
                plt.text(infos['coordinates'][value][0], infos['coordinates'][value][1], str(value), fontsize=fontsize, verticalalignment='center', horizontalalignment='center')
    
    @staticmethod
    def __plotLine(lines, ax):
        for line in lines:
            line = mlines.Line2D(line[0], line[1],lw=3, ls='-')
            line.set_zorder(0)
            ax.add_line(line)
            
    @classmethod
    def __plotTree(cls, redblacktree):
        node_infos = cls.__getNodeInfos(redblacktree)
        lines = cls.__getLineCoordinate(redblacktree, node_infos)
        fig,ax = plt.subplots()
        cls.__plotCircle(node_infos, ax)
        cls.__plotLine(lines, ax)
        plt.axis('off')
        plt.axis('equal')
        return plt
    
    @classmethod
    def showTree(cls, redblacktree):
        plt = cls.__plotTree(redblacktree)
        plt.show()
        
    @classmethod
    def saveTree(cls, redblacktree, path, name):
        plt = cls.__plotTree(redblacktree)
        plt.savefig(path + name + '.png', dpi=500)