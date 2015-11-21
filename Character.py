from Object import *



class Animation:
    def __init__(self, img, frame, w, h):
        self.animImage = load_image(img)
        self.frame = frame
        self.w, self.h = w, h


# class Character(GameObject):
#     def __init__(self):
#         super().__init__()
#         self.currentAnimation = None
#         self.frame = 0
#         self.state = None
#         self.isDelete = False
#         self.colBox = None
#         self.vx, self.vy = 0, 0
#         return
#
#     def ChangeState(self, newState):
#         if self.state is not None:
#             self.state.Exit(self)
#         self.state = self.stateList[newState]
#         self.state.Enter(self)
#
#     def Update(self, frame_time):
#         if self.state is not None:
#             self.state.Update(self, frame_time)
#
#     def Draw(self, frame_time):
#         if self.state is not None:
#             self.state.Draw(self, frame_time)
#
#     def Collision(self, other, frame_time):
#         if self.state is not None:
#             self.state.Collision(self, other, frame_time)
