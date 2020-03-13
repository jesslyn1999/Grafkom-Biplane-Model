from .Primitives import Transform
from abc import ABC, abstractmethod
from OpenGL.GL import glPushMatrix, glPopMatrix

class Tag:

    def __init__(self):
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def has_tag(self, tag):
        return tag in self.tags

class LSObject:

    def get_transform(self):
        return self._transform

    transform = property(get_transform, None)

    def get_component(self, T):
        comp = None
        for component in self.components:
            if isinstance(component, T):
                comp = component
                break
        return comp

    def __init__(self, clone=None):
        self.components = []
        self.enabled = True
        self.tag = Tag()
        if clone:
            if isinstance(clone, str):
                self.name = clone
                self._transform = Transform()
                self._transform.owner = self
                self.PreRender = lambda: None
            else:
                self.name = clone.name
                self._transform = Transform(clone.transform.position, clone.transform.rotation)
                self._transform.owner = self
                self.PreRender = clone.PreRender
                self.enabled = clone.enabled
                self.tag.tags.extend(clone.tag.tags)

                for component in clone.components:
                    self.add_component(component.clone())

                # Clone the childs as well.
                for child in clone.transform.childs:
                    clonedChild = child.owner.clone()
                    clonedChild.transform.setParent(self.transform)
        else:
            self.name = "Unnamed"
            self._transform = Transform()
            self._transform.owner = self
            self.PreRender = lambda: None
        

    def add_component(self, component):
        self.components.append(component)
        component.owner = self
        component.enable()

    def clone(self):
        return LSObject(self)

    def message(self, message, *args):
        if self.enabled:
            for component in self.components:
                if hasattr(component, message):
                    getattr(component, message)(*args)
            # Clone the childs as well.
            for child in self.transform.childs:
                child.owner.message(message, *args)

    def update(self):
        if self.enabled:
            for component in self.components:
                if hasattr(component, "update"):
                    component.update()
            # Update the childs as well.
            for child in self.transform.childs:
                child.owner.update()
                
    def pre_render(self):
        if self.enabled:
            glPushMatrix()
            self.transform.apply()

            for component in self.components:
                if hasattr(component, "pre_render"):
                    component.pre_render()
            
            glPopMatrix()

            # Renders the childs as well.
            for child in self.transform.childs:
                child.owner.pre_render()

    def post_render(self):
        if self.enabled:
            glPushMatrix()
            self.transform.apply()

            for component in self.components:
                if hasattr(component, "post_render"):
                    component.post_render()
            
            glPopMatrix()

            # Renders the childs as well.
            for child in self.transform.childs:
                child.owner.post_render()

    def render(self):
        if self.enabled:
            glPushMatrix()
            self.transform.apply()

            self.PreRender()

            for component in self.components:
                if hasattr(component, "render"):
                    component.render()
            
            glPopMatrix()

            # Renders the childs as well.
            for child in self.transform.childs:
                child.owner.render()

    def __str__(self):
        return self.name


class Component(ABC):

    owner = None
    enabled = False

    def enable(self):
        if not self.enabled:
            if hasattr(self, "on_enabled"):
                getattr(self, "on_enabled")()
        self.enabled = True

    def disable(self):
        if self.enabled:
            if hasattr(self, "on_disabled"):
                getattr(self, "on_disabled")()
        self.enabled = False

    @abstractmethod
    def clone(self):
        pass

