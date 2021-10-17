

class Node:

    def __init__(self,val):
        self.val=val
        self.left=None
        self.right=None
        self.ln=0
        self.rn=0
        self.height=1
        self.parent=None


class Avl_tree:

    def __init__(self):
        self.root=None

    def insert(self,val):
        if self.root==None:
            self.root=Node(val)
        else:
            self.__insert(self.root,val)

    def __insert(self,curr,val):

        if curr.val>val:
            if curr.left==None:
                curr.left=Node(val)
                curr.left.parent=curr
                self._inspect_insertion(curr.left)
                self.upd(curr.left)
            else:
                self.__insert(curr.left,val)
        elif curr.val<val:
            if curr.right==None:
                curr.right=Node(val)
                curr.right.parent=curr
                self._inspect_insertion(curr.right)
                self.upd(curr.right)
            else:
                self.__insert(curr.right,val)
        return

    def height(self):
        if self.root!=None:
            return self.__height(self.root,0)
        return 0

    def __height(self,curr,h):
        if curr==None:
            return h
        l=self.__height(curr.left,h+1)
        r=self.__height(curr.right,h+1)
        return max(l,r)

    def find(self,val):
        if self.root!=None:
            return self.__find(self.root,val)
        return None

    def __find(self,curr,val):
        if curr==None:
            return None
        if curr.val==val:
            return curr
        if curr.val>val:
            return self.__find(curr.left,val)
        return self.__find(curr.right,val)

    def delete(self,val):
        self.delete_node(self.find(val))

    def delete_node(self,curr):

        if curr==None or self.find(curr.val)==None:
            return None

        def min_val(n):
            current=n
            while current.left!=None:
                current=current.left
            return current

        def num_children(node):
            if node.left!=None and node.right!=None:
                return 2
            if node.left!=None or node.right!=None:
                return 1
            return 0

        curr_par=curr.parent
        curr_child=num_children(curr)

        if curr_child==0:
            if curr.parent!=None:
                if curr_par.left==curr:
                    curr.parent.left=None
                else:
                    curr.parent.right=None
            else:
                self.root=None

        if curr_child==1:

            if curr.left!=None:
                child=curr.left
            else:
                child=curr.right

            if curr.parent!=None:
                if curr_par.left==curr:
                    curr_par.left=child
                else:
                    curr_par.right=child
            else:
                self.root=child

        if curr_child==2:
            successor=min_val(curr.right)
            curr.val=successor.val
            self.delete_node(successor)
            self.upd(curr)
            return

        if curr_par!=None:
            curr_par.height=1+max(self.get_height(curr_par.left),self.get_height(curr_par.right))
            self._inspect_del(curr.parent)
            self.upd(curr.parent)

    def search(self,val):
        if self.root==None:
            return False
        return self.__search(self.root,val)

    def __search(self,curr,val):
        if curr==None:
            return False
        if curr.val==val:
            return True
        if curr.val>val:
            return self.__search(curr.left,val)
        return self.__search(curr.right,val)

    def _inspect_insertion(self,curr,path=[]):
        if curr.parent==None:
            return
        path=[curr]+path
        lh=self.get_height(curr.parent.left)
        rh=self.get_height(curr.parent.right)
        if abs(lh-rh)>1:
            path=[curr.parent]+path

            self.rebalance(path[0],path[1],path[2])
            self.upd(curr)
            return
        newh=1+curr.height
        if newh>curr.parent.height:
            curr.parent.height=newh
        self._inspect_insertion(curr.parent,path)
        self.upd(curr.parent)

    def _inspect_del(self,curr):
        if curr==None:
            return
        lh=self.get_height(curr.left)
        rh=self.get_height(curr.right)
        if abs(lh-rh)>1:
            y=self.taller(curr)
            x=self.taller(y)
            self.rebalance(curr,y,x)

        self._inspect_del(curr.parent)

    def rebalance(self,z,y,x):

        if y==z.left and x==y.left:
            self.right_rotate(z)

        elif y==z.left and x==y.right:
            self.left_rotate(y)
            self.right_rotate(z)

        elif y==z.right and x==y.right:
            self.left_rotate(z)

        elif y==z.right and x==y.left:
            self.right_rotate(y)
            self.left_rotate(z)
        return

    def right_rotate(self,z):

        sub=z.parent
        y=z.left
        t=y.right
        y.right=z
        z.parent=y
        z.left=t
        if t!=None:
            t.parent=z
        y.parent=sub
        if y.parent==None:
            self.root=y
        else:
            if y.parent.left==z:
                y.parent.left=y
            else:
                y.parent.right=y
        z.height=1+max(self.get_height(z.left),self.get_height(z.right))
        y.height=1+max(self.get_height(y.right),self.get_height(y.left))

    def left_rotate(self,z):
        sub = z.parent
        y = z.right
        t = y.left
        y.left = z
        z.parent = y
        z.right = t
        if t != None:
            t.parent = z
        y.parent = sub
        if y.parent == None:
            self.root = y
        else:
            if y.parent.left == z:
                y.parent.left = y
            else:
                y.parent.right = y
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.right), self.get_height(y.left))

    def get_height(self,curr):
        if curr==None:
            return 0
        return curr.height

    def taller(self,curr):
        l,r=self.get_height(curr.left),self.get_height(curr.right)
        if l>=r:
            return curr.left
        return curr.right

    def upd(self,curr):
        if curr.left!=None:
            self.__upd(curr.left)
        else:
            curr.ln=0
        if curr.right!=None:
            self.__upd(curr.right)
        else:
            curr.rn=0
        self.__upd(curr)

    def __upd(self,curr):
        while curr!=None:
            if curr.left!=None:
                curr.ln=curr.left.ln+curr.left.rn+1
            else:
                curr.rn=0
            if curr.right!=None:
                curr.rn=curr.right.rn+curr.right.ln+1
            else:
                curr.rn=0
            curr=curr.parent



