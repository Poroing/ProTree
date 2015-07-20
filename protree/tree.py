from math import pi
from enum import IntEnum
from collections import namedtuple
from random import choice, uniform, randint

class Tree(object):
    """Object that represent a tree formed of other trees that represent branch

    Attributes:
        branches: store all the branch of the tree
        last_branches: generator that iterate on the branch that don't have
            any branch on them
    """

    Branch = namedtuple('Branch', 'tree, height, angle, ratio')
    """store the branch and his relationship with the tree"""

    def __init__(self):
        self.branches = []

    @property
    def last_branches(self):
        """Yield the branches with no branches on them"""
        if self.branches == []:
            yield self
        else:
            for branch in self:
                for last_branch in branch.last_branches:
                    yield last_branch

    def addBranch(self, height, angle, branch_trunk_ratio=0.5):
        """Add one branch at the tree

        Add a branch with size of the tree times branch_trunk_ratio in the tree
        at the given height and the given angle.

        Args:
            height: the position of the branch on the tree.
            angle: The angle the branch make with the tree
            branch_trunk_ratio: the ratio between the size of the tree and the
                branch. default value: 0.5
        """
        self.branches.append(Tree.Branch(Tree(), height, angle,
            branch_trunk_ratio))

    def __getitem__(self, key):
        """Return the key'th branch without his property

        Args:
            key: an integer that indicate the place of the branch in the tree

        Return:
            A Tree object representing the key'th branch of the tree

        Raise:
            IndexError: the key passed is negative or greater than len(branches)
        """
        try:
            return self.branches[key].tree
        except Exception:
            raise

    def __len__(self):
        """Return the height of the tree

        The height returned is the distance between the inner branches and the
            tree

        Return:
            the distance between the inner branches and the tree
        """
        if self.branches == []:
            return 1
        return 1 + max(map(len, self))

    def __repr__(self):
        return 'Tree: {} branch'.format(len(self.branches))

class TreeBuilder(object):
    """Object that develop a Tree object with proceduraly created branch

    TreeBuilder store all the value that define how it will develop a Tree

    Attributes:
        min_branch: An integer indicating the minimum number of branch to be
            added to a Tree
        max_branch: An integer indicating the maximum number of branch to be
            added to a Tree
        top_branch: A boolean indicating if a branch will be added in addition
            of the other branches
        top_branch_height: A float in the range [0,1] indicating where the top
            branch will be added on the tree
        branch_trunk_ratio: A float which value is the size of the branch that
            will be added over the size of the tree at which the branches are
            added
        random_side: A boolean indicating if each branch should be put
            atenatively on the right side and left side or should be put on
            completely random side
        base_branch_angle: A float indicating in radiant the base angle the
            added branch will do with the tree
        min_branch_angle: A float indicating in radiant the minimum value added
            to the base angle to define the final angle which the branches do
            with the tree
        max_branch_angle: A float indicating in radiant the maximum value added
            to the base angle to define the final angle which the branches do
            with the tree
        min_branch_height: A float in the range [0,1] indicating the lowest
            place at which the branch will be added on the tree, where 0 is the
            base of the tree and 1 is the top.
        max_branch_height: A float in the range [0,1] indicating the highest
            place at which the branch will be added on the tree, where 0 is the
            base of the tree and 1 is the top.
    """

    def __init__(self, 
        min_branch=2, max_branch=5,
        top_branch=True, top_branch_height=0.95,
        branch_trunk_ratio=0.6,
        random_side=False,
        base_branch_angle=pi / 4,
        min_branch_angle=-pi / 6, max_branch_angle=pi / 6,
        min_branch_height=0.5, max_branch_height=0.9):

        self.min_branch = min_branch 
        self.max_branch = max_branch 
        self.top_branch = top_branch 
        self.top_branch_height = top_branch_height
        self.branch_trunk_ratio = branch_trunk_ratio 
        self.base_branch_angle = base_branch_angle 
        self.random_side = random_side
        self.min_branch_angle = min_branch_angle 
        self.max_branch_angle = max_branch_angle 
        self.min_branch_height = min_branch_height 
        self.max_branch_height = max_branch_height

    def addBranches(self, tree, time=1):
        """Add branches to the trunk time times on tree

        Args:
            tree: The Tree to which add the branches.
            time: The number of time the builder should recursively add
                branches to the tree.
                
                For example:
                builder.addBranches(tree, 3)
                Will add some branches to the trunk of tree, and then add
                branches to each created branches and do that once again with
                the newly created branches.
        """

        current_side = choice([-1, 1]) #-1 : Left, 1 : Right
        for i in range(randint(self.min_branch, self.max_branch)):
            branch_height = self.randomHeight()
            branch_angle = self.randomBaseAngle() * current_side

            tree.addBranch(branch_height, branch_angle, self.branch_trunk_ratio)

            current_side = choice([-1, 1]) if self.random_side else -current_side

        tree.addBranch(self.top_branch_height, self.randomAngle(),
            self.branch_trunk_ratio)

        if time > 1:
            for branch in tree:
                self.addBranches(branch, time - 1)

    def addBranchesToEnd(self, tree, time=1):
        """Add branches to the last branches of the tree

        Args:
            tree: The Tree to which add branches to the last branches
            time: The number of time the builder should recursively add
                branches

                It will add the branches, and then add branches to the newly
                created branches, this time times
        """
        for branch in tree.last_branches:
            self.addBranches(branch, time)

    def randomHeight(self):
        return uniform(self.min_branch_height, self.max_branch_height)

    def randomAngle(self):
        return uniform(self.min_branch_angle, self.max_branch_angle)

    def randomBaseAngle(self):
        return self.base_branch_angle + self.randomAngle()

if __name__ == '__main__':
    tree = Tree()
    for i in range(4):
        tree.branches.append(Tree.Branch(Tree(), 0, 0, 0))
        for j in range(4):
            tree.branches[i].tree.branches.append(Tree.Branch(Tree(), 0, 0, 0))

    for last_child in tree.last_branches:
        for i in range(4):
            last_child.branches.append(Tree.Branch(Tree(), 0, 0, 0))
