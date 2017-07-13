#!/usr/bin/env python
import operator
import math
import rospy
from threespace.msg import dataVec
from Quatmath import sub
from Quatmath import add
from skeleton.msg import jointAngles
from skeleton.msg import gyroQuat
from std_msgs.msg import String

class Skeleton:
    def __init__(self,segments, name):
        self.segments = segments
        self.name=name
        self.pub = rospy.Publisher('joints', jointAngles, queue_size=1)
        self.pubg = rospy.Publisher('gyro', gyroQuat, queue_size=1)
        self.node = rospy.init_node('skeleton_node', anonymous=True)
        self.jointAngle_msg = jointAngles()
        self.gyro_msg = gyroQuat()         
        #for k in list(self.segments):
        #    for i in list(self.segments[k]): 
        #        self.segments[k][i].pub = rospy.Publisher(k+'_'+self.segments[k][i].name, jointAngles, queue_size=1)
        #        self.segments[k][i].node=rospy.init_node(k+'_'+self.segments[k][i].name+'_node', anonymous=True)
        #        message = jointAngles(Intervertebral=[1,0,0,0])
        #        self.segments[k][i].pub.publish(message) 

    def update(self):
        origin = self.segments['Trunk']['root'].IMU.origin
        for k in list(self.segments):
            for i in list(self.segments[k]):
                if (self.segments[k][i].IMU_attached == 1):
                    self.segments[k][i].quat=self.segments[k][i].IMU.quat
                    self.segments[k][i].gyro=self.segments[k][i].IMU.gyro
                    self.segments[k][i].IMU.origin = origin
        #        else:
        #            self.segments[k][i].quat=[1,0,0,0]
                    #print(skeleton.segments[k][i].quat)
        stack = [['Trunk','root']]
        while(len(stack)>0):
            child = stack.pop()
            while(child[1] != 0):
                joint = self.segments[child[0]][child[1]]
                child=joint.child[0]
                parent = joint.parent
                if (joint.IMU_attached ==0):
			joint.quat = self.segments[parent[0]][parent[1]].quat
                        joint.gyro = self.segments[parent[0]][parent[1]].gyro
                joint.angle = sub.sub(joint.quat,self.segments[parent[0]][parent[1]].quat)
                joint.vel = sub.sub(joint.gyro,self.segments[parent[0]][parent[1]].gyro)
                if (joint.name=='root'):
                    joint.angle = joint.quat
                    joint.vel = joint.gyro
                    #print(joint.name)
                    #print(joint.quat)
                #joint.quat = add.add(joint.quat,self.segments[parent[0]][parent[1]].quat)
                #print(joint.quat)
                L = len(joint.child)
                if (L>2):
                    for i in range(1,L):
                        stack.append(joint.child[i])
                        joint1 = self.segments[joint.child[i][0]][joint.child[i][1]]
                        #print(joint.name)
			child1=joint1.child[0]
                        parent1 = joint1.parent
                        if (joint1.IMU_attached ==0):
			    joint1.quat = self.segments[parent[0]][parent[1]].quat
                            joint1.gyro = self.segments[parent[0]][parent[1]].gyro
                        joint1.angle = sub.sub(joint1.quat,self.segments[parent[0]][parent[1]].quat)
                        joint1.vel = sub.sub(joint1.gyro,self.segments[parent[0]][parent[1]].gyro)
                        #print(joint.quat)
            for k in list(self.segments):
                for i in list(self.segments[k]):
                    if (self.segments[k][i].IMU_attached == 0):
                        #self.segments[k][i].quat=[1,0,0,0]
			#self.segments[k][i].angle=[1,0,0,0]
                        pass
                   # if(self.segments[k][i].name=='Elbow_R'):
                    #    print(self.segments[k][i].quat)
                    if (self.segments[k][i].IMU_attached == 1):  
                        q = self.segments[k][i].angle
                           # self.segments[k][i].angle = [q[0],q[1],q[3],q[2]]
                    setattr(self.jointAngle_msg,k+'_'+i,self.segments[k][i].angle)
                    setattr(self.gyro_msg,k+'_'+i,self.segments[k][i].vel)                       
                 
            self.pub.publish(self.jointAngle_msg)
            #self.pubg.publish(self.gyro_msg)
            #print(self.jointAngle_msg)
    def addParents(self):
        stack = [['Trunk','base']]
      #  joint = self.segments[stack[0][0]][stack[0][1]]
       # joint.parent = stack[0]
        while(len(stack)>0):
            #print(stack)
            child = stack.pop()
            while(child[1] != 0): 
                joint = self.segments[child[0]][child[1]]
                #print(joint.name)
                seg = child[0]
                child=joint.child[0]
                try:
                    child_joint = self.segments[child[0]][child[1]]
                    child_joint.parent = [seg,joint.name]
                    #print(child_joint.parent)
                    #print(child_joint.name)
                except:
                    #print(child_joint.name)
                    pass
                if (len(joint.child)>2):
                    for i in range(1,len(joint.child)):      
                        stack.append(joint.child[i])
                        self.segments[joint.child[i][0]][joint.child[i][1]].parent = [seg,joint.name]
class imu():
    offset = [1,0,0,0]
    origin = [1,0,0,0]
    def __init__(self,topic):
        self.quat = [1,0,0,0]
        self.gyro = [1,0,0,0]
	#self.origin = [1,0,0,0]
        self.topic=topic
        #self.node=rospy.init_node('IMU_listener', anonymous=True)
        
        self.sub=rospy.Subscriber(topic+'_data_vec', dataVec, self.callback,queue_size=1)       
        self.subC = rospy.Subscriber('/recognizer/output', String,self.checkCalibrate, queue_size=1)
        # spin() simply keeps python from exiting until this node is stopped
        #rospy.spin()
    def callback(self,data):
        rospy.set_param("/Skeleton_node"+self.topic+'_IMU', 1)
        #self.data= data
        #print(self.offset)
        #r = rospy.Rate(120)
        #r.sleep()
        #print(data.transforms[0].child_frame_id)
        #if(data.transforms[0].child_frame_id==self.str):
        #print('test')
        self.orientation = data.quat.quaternion
        gyro = [data.gyroX,data.gyroY,data.gyroZ]
        theta = math.sqrt(gyro[0]**2+gyro[1]**2+gyro[2]**2)/(80)
        n = math.sqrt(gyro[0]**2+gyro[1]**2+gyro[2]**2)
        q0 = math.cos(theta/2)
        s = math.sqrt(1-q0**2)
        qy = (gyro[0]/n)*s
        qz = -(gyro[1]/n)*s
        qx = -(gyro[2]/n)*s
        #self.gyro = [q0,qx,qy,qz]
        #print(self.q_gyro)
        #self.quat = sub.sub(add.add([self.orientation.w,self.orientation.z,self.orientation.x,self.orientation.y],self.offset),self.offset)
        #self.quat = sub.sub([self.orientation.w,self.orientation.z,self.orientation.x,self.orientation.y],self.offset)
        #self.quat = sub.sub(add.add(self.offset,[self.orientation.w,self.orientation.z,self.orientation.x,self.orientation.y]),[1,0,0,0])
        #self.quat = sub.sub(add.add(sub.sub([1,0,0,0],self.offset),[self.orientation.w,self.orientation.z,self.orientation.x,self.orientation.y]),self.offset)
        self.quat = add.add([self.orientation.w,self.orientation.z,self.orientation.x,self.orientation.y],sub.sub(self.origin,self.offset))
        self.gyro = sub.sub(self.offset,add.add([q0,qz,qx,qy],sub.sub([1,0,0,0],self.offset)))
            #self.quat = [orientation.w,orientation.y,orientation.z,orientation.x]
        #self.roll = math.atan2(2*self.quat[3]*self.quat[0]+2*self.quat[1]*self.quat[2],1-2*self.quat[0]**2-2*self.quat[1]**2)
        #self.pitch = math.asin(2*self.quat[3]*self.quat[1]-2*self.quat[2]*self.quat[0])
        #self.yaw = math.atan2(2*self.quat[3]*self.quat[2]+2*self.quat[0]*self.quat[1],1-2*self.quat[1]**2-2*self.quat[2]**2)
    def shutdown(self):
        print(self.topic)
        rospy.signal_shutdown('user terminated')

    def checkCalibrate(self,data):
        rospy.set_param("/Skeleton_node"+self.topic+'_IMU', 1)
        #r = rospy.Rate(10)
        #r.sleep()
        if (data.data =='start calibrate'):
            #print('test') 
            self.Calibrate()  

    def Calibrate(self):
        try:
            self.offset=[self.orientation.w,self.orientation.z,self.orientation.x,self.orientation.y]
            if (self.topic =='/temp_4'):
                self.origin = [1,0,0,0] # needs work
            print('calibarted')
            print(self.offset)
        except:
            pass 

class Joint:
    def __init__(self,movements,limitM,limitm,name,num):
        self.angle = [1,0,0,0]
        self.quat = [1,0,0,0]
        self.gyro = [1,0,0,0]
        self.vel = [1,0,0,0]
        self.name=name
        self.movements = movements
        self.num=num
        self.limitM=limitM
        self.limitm=limitm
        self.IMU_attached = 0
        self.child = [[0,0]]
        self.parent = [0,0]
        self.pub=[]
        self.node = []
    def addIMU(self,IMU):
        self.IMU = IMU
        self.IMU_attached = 1
    def flexion(self,rot):
        if("flexion" in self.movements):
            rot = rot/self.num
            self.angle = [rot,self.angle[1],self.angle[2]]
            self.AngleLimit()
    def extension(self,rot):
        if("extension" in self.movements):
            rot = -rot/self.num
            self.angle = [rot,self.angle[1],self.angle[2]]
            self.AngleLimit()
    def abduction(self,rot):
        if(self.name[len(self.name)-1]=='L'):
            rot=-rot
        if("abduction" in self.movements) + ("lateral flexion" in self.movements):
            rot = rot/self.num
            self.angle = [self.angle[0],self.angle[1],rot]
            self.AngleLimit()
    def adduction(self,rot):
        if(self.name[len(self.name)-1]=='L'):
            rot=-rot
        if("abduction" in self.movements) + ("lateral flexion" in self.movements):
            rot = -rot/self.num
            self.angle = [self.angle[0],self.angle[1],rot]
            self.AngleLimit()
    def rotation(self,rot):
        if("rotation" in self.movements):
            rot = rot/self.num
            self.angle = [self.angle[0],rot,self.angle[2]]
            self.AngleLimit()
    def AngleLimit(self):
        if self.angle[0]>self.limitM[0]/self.num:
            self.angle = [self.limitM[0]/self.num,self.angle[1],self.angle[2]]
        if self.angle[1]>self.limitM[1]/self.num:
            self.angle = [self.angle[0],self.limitM[1]/self.num,self.angle[2]]
        if self.angle[2]>self.limitM[2]/self.num:
            self.angle = [self.angle[0],self.angle[1],self.limitM[2]/self.num]
        if self.angle[0]<self.limitm[0]/self.num:
            self.angle = [self.limitm[0]/self.num,self.angle[1],self.angle[2]]
        if self.angle[1]<self.limitm[1]/self.num:
            self.angle = [self.angle[0],self.limitm[1]/self.num,self.angle[2]]
        if self.angle[2]<self.limitm[2]/self.num:
            self.angle = [self.angle[0],self.angle[1],self.limitm[2]/self.num]
# anitomical movements            
Intervertebral_movements = ['flexion', 'extension', 'hyperextension', 'lateral flexion', 'rotation', 'circumduction']
Atlantoaxial_movements = ['rotation']
Shoulder_movements = ['flexion', 'extension', 'hyperextension', 'abduction', 'adduction','rotation','hyperabduction', 'hyperadduction', 'horizontal abduction', 'horizontal adduction', 'med/lat rotation', 'circumduction']
Sternoclavicular_movements =['elevation', 'depression', 'abduction', 'adduction', 'protraction', 'retraction', 'rotation']
Acromioclavicular_movements =['abduction', 'adduction', 'protraction', 'retraction', 'upward/downward rotation']
Elbow_movements =['flexion', 'extension', 'hyperextension']
Radioulnar_movements =['pronation', 'supination']
Wrist_movements =['flexion', 'extension', 'hyperextension', 'radial flexion', 'ulnar flexion', 'circumduction']
Metacarpophalangeal_movements =['flexion', 'extension', 'hyperextension', 'abduction', 'adduction', 'circumduction']
Interphalangeal_movements =['flexion', 'extension', 'hyperextension']
Carpometacarpal_movements =['flexion', 'extension', 'abduction', 'adduction', 'opposition', 'circumduction']
Hip_movements =['flexion', 'extension', 'hyperextension', 'abduction', 'adduction', 'hyperadduction', 'horizontal adduction', 'horizontal abduction', 'med/lat rotation', 'circumduction']
Knee_movements =['flexion', 'extension', 'hyperextension', 'med/lat rotation']
Ankle_movements =['plantarflexion', 'dorsiflexion','flexion', 'extension', 'abduction', 'adduction','rotation']
Intertarsal_movements =['inversion', 'eversion']
Metatarsophalangeal_movements =['flexion', 'extension', 'abduction', 'adduction', 'circumduction']
# segments
pi = 3.1415926535897932384626433832795
k = pi/180
Head_joints = {'Intervertebral':Joint(Intervertebral_movements,[k*70,k*70,k*35], [-k*55,-k*70,-k*35],'Intervertebral',2),'Atlantoaxial':Joint(Atlantoaxial_movements,[1,1,1], [-1,-1,-1],'Atlantoaxial',1)}
Trunk_joints = {'base':Joint(Intervertebral_movements,[k*180,k*180,k*180], [-k*180,-k*180,--k*180],'root',1),'root':Joint(Intervertebral_movements,[k*180,k*180,k*180], [-k*180,-k*180,--k*180],'root',1),'Intervertebral1':Joint(Intervertebral_movements,[k*15,k*8,k*18], [-k*35,-k*12,-k*18],'Intervertebral1',1),'Intervertebral2':Joint(Intervertebral_movements,[k*7,k*8,k*18], [-k*7,-k*12,-k*18],'Intervertebral2',1),'Intervertebral3':Joint(Intervertebral_movements,[k*7,k*8,k*18], [-k*7,-k*12,-k*18],'Intervertebral3',1),'Intervertebral4':Joint(Intervertebral_movements,[k*7,k*8,k*18], [-k*7,-k*12,-k*18],'Intervertebral4',1),'Intervertebral5':Joint(Intervertebral_movements,[k*75,k*35,k*18], [-k*30,-k*35,-k*18],'Intervertebral5',1)}
Arm_joints = {'Shoulder_R':Joint(Shoulder_movements,[k*130,k*180,k*90], [-k*45,-k*60,-k*135],'Shoulder_R',2),'Shoulder_L':Joint(Shoulder_movements,[k*130,k*60,k*90], [-k*45,-k*180,-k*135],'Shoulder_L',2)}
Shoulder_joints = {'Sternoclavicular_R':Joint(Sternoclavicular_movements,[1,1,1], [-1,-1,-1],'Sternoclavicular_R',1),'Sternoclavicular_L':Joint(Sternoclavicular_movements,[1,1,1], [-1,-1,-1],'Sternoclavicular_L',1)}
Girdle_joints = {'Acromioclavicular_R':Joint(Acromioclavicular_movements,[1,1,1], [-1,-1,-1],'Acromioclavicular_R',1),'Acromioclavicular_L':Joint(Acromioclavicular_movements,[1,1,1], [-1,-1,-1],'Acromioclavicular_L',1)}
Forearm_joints ={'Elbow_R':Joint(Elbow_movements,[1,1,1], [-1,-1,-1],'Elbow_R',1),'Radioulnar_R':Joint(Radioulnar_movements,[1,1,1], [-1,-1,-1],'Radioulnar_R',1),'Elbow_L':Joint(Elbow_movements,[1,1,1], [-1,-1,-1],'Elbow_L',1),'Radioulnar_L':Joint(Radioulnar_movements,[1,1,1], [-1,-1,-1],'Radioulnar_L',1)}
Hand_joints = {'Wrist_R':Joint(Wrist_movements,[1,1,1], [-1,-1,-1],'Wrist_R',1),'Wrist_L':Joint(Wrist_movements,[1,1,1], [-1,-1,-1],'Wrist_L',1)}
Fingers_joints = {}
Fingers_joints1 ={'Metacarpophalangeal1_R':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal1_R',1),'Interphalangeal1_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal1_R',1),'Metacarpophalangeal1_L':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal1_L',1),'Interphalangeal1_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal1_L',1)}
Fingers_joints.update(Fingers_joints1)
Fingers_joints2 ={'Metacarpophalangeal2_R':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal2_R',1),'Interphalangeal2_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal2_R',1),'Metacarpophalangeal2_L':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal2_L',1),'Interphalangeal2_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal2_L',1)}
Fingers_joints.update(Fingers_joints2)
Fingers_joints3 ={'Metacarpophalangeal3_R':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal3_R',1),'Interphalangeal3_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal3_R',1),'Metacarpophalangeal3_L':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal3_L',1),'Interphalangeal3_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal3_L',1)}
Fingers_joints.update(Fingers_joints3)
Fingers_joints4 ={'Metacarpophalangeal4_R':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal4_R',1),'Interphalangeal4_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal4_R',1),'Metacarpophalangeal4_L':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal4_L',1),'Interphalangeal4_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal4_L',1)}
Fingers_joints.update(Fingers_joints4)
Thumb_joints ={'Carpometacarpal_R':Joint(Carpometacarpal_movements,[1,1,1], [-1,-1,-1],'Carpometacarpal_R',1),'Metacarpophalangeal_R':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal_R',1),'Interphalangeal_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal_R',1),'Carpometacarpal_L':Joint(Carpometacarpal_movements,[1,1,1], [-1,-1,-1],'Carpometacarpal_L',1),'Metacarpophalangeal_L':Joint(Metacarpophalangeal_movements,[1,1,1], [-1,-1,-1],'Metacarpophalangeal_L',1),'Interphalangeal_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal_L',1)}
Thigh_joints ={'Hip_R':Joint(Hip_movements,[1,1,1], [-1,-1,-1],'Hip_R',1),'Hip_L':Joint(Hip_movements,[1,1,1], [-1,-1,-1],'Hip_L',1)}
Leg_joints = {'Knee_R':Joint(Knee_movements,[1,1,1], [-1,-1,-1],'Knee_R',1),'Knee_L':Joint(Knee_movements,[1,1,1], [-1,-1,-1],'Knee_L',1)}
Foot_joints ={'Ankle_R':Joint(Ankle_movements,[1,1,1], [-1,-1,-1],'Ankle_R',1),'Ankle_L':Joint(Ankle_movements,[1,1,1], [-1,-1,-1],'Ankle_L',1),'Intertarsal_R':Joint(Intertarsal_movements,[1,1,1], [-1,-1,-1],'Intertarsal_R',1),'Intertarsal_L':Joint(Intertarsal_movements,[1,1,1], [-1,-1,-1],'Intertarsal_L',1)}
Toes_joints = {}
Toes_joints1 ={'Metatarsophalangeal1_R':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal1_R',1),'Interphalangeal1_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal1_R',1),'Metatarsophalangeal1_L':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal1_L',1),'Interphalangeal1_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal1_L',1)}
Toes_joints.update(Toes_joints1)
Toes_joints2 ={'Metatarsophalangeal2_R':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal2_R',1),'Interphalangeal2_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal2_R',1),'Metatarsophalangeal2_L':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal2_L',1),'Interphalangeal2_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal2_L',1)}
Toes_joints.update(Toes_joints2)
Toes_joints3 ={'Metatarsophalangeal3_R':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal3_R',1),'Interphalangeal3_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal3_R',1),'Metatarsophalangeal3_L':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal3_L',1),'Interphalangeal3_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal3_L',1)}
Toes_joints.update(Toes_joints3)
Toes_joints4 ={'Metatarsophalangeal4_R':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal4_R',1),'Interphalangeal4_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal4_R',1),'Metatarsophalangeal4_L':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal4_L',1),'Interphalangeal4_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal4_L',1)}
Toes_joints.update(Toes_joints4)
Toes_joints5 ={'Metatarsophalangeal5_R':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal5_R',1),'Interphalangeal5_R':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal5_R',1),'Metatarsophalangeal5_L':Joint(Metatarsophalangeal_movements,[1,1,1], [-1,-1,-1],'Metatarsophalangeal5_L',1),'Interphalangeal5_L':Joint(Interphalangeal_movements,[1,1,1], [-1,-1,-1],'Interphalangeal5_L',1)}
Toes_joints.update(Toes_joints5)
############################################333S

segments = {'Head':Head_joints,'Trunk':Trunk_joints,'Arm':Arm_joints,'Shoulder':Shoulder_joints,'Girdle':Girdle_joints,'Forearm':Forearm_joints,'Hand':Hand_joints,'Fingers':Fingers_joints,'Thumb':Thumb_joints,'Thigh':Thigh_joints,'Leg':Leg_joints,'Foot':Foot_joints,'Toes':Toes_joints}
skeleton = Skeleton(segments,'Male')
# links
skeleton.segments['Trunk']['base'].child =[['Trunk','root']]
skeleton.segments['Trunk']['root'].child =[['Trunk','Intervertebral1']]
skeleton.segments['Trunk']['Intervertebral1'].child = [['Trunk','Intervertebral2'],['Thigh','Hip_L'],['Thigh','Hip_R']]
skeleton.segments['Trunk']['Intervertebral2'].child =[['Trunk','Intervertebral3']]
skeleton.segments['Trunk']['Intervertebral3'].child =[['Trunk','Intervertebral4']]
skeleton.segments['Trunk']['Intervertebral4'].child =[['Trunk','Intervertebral5']]
skeleton.segments['Trunk']['Intervertebral5'].child =[['Head','Intervertebral'],['Shoulder','Sternoclavicular_L'],['Shoulder','Sternoclavicular_R']]    
skeleton.segments['Head']['Intervertebral'].child = [['Head','Atlantoaxial']] 
skeleton.segments['Shoulder']['Sternoclavicular_L'].child = [['Girdle','Acromioclavicular_L']]
skeleton.segments['Girdle']['Acromioclavicular_L'].child = [['Arm','Shoulder_L']]
skeleton.segments['Arm']['Shoulder_L'].child = [['Forearm','Elbow_L']] 
skeleton.segments['Forearm']['Elbow_L'].child = [['Forearm','Radioulnar_L']]
skeleton.segments['Forearm']['Radioulnar_L'].child = [['Hand','Wrist_L']]
skeleton.segments['Hand']['Wrist_L'].child = [['Thumb','Carpometacarpal_L'],['Fingers','Metacarpophalangeal1_L'],['Fingers','Metacarpophalangeal2_L'],['Fingers','Metacarpophalangeal3_L'],['Fingers','Metacarpophalangeal4_L']]
skeleton.segments['Thumb']['Carpometacarpal_L'].child = [['Thumb','Metacarpophalangeal_L']]
skeleton.segments['Thumb']['Metacarpophalangeal_L'].child = [['Thumb','Interphalangeal_L']]
skeleton.segments['Fingers']['Metacarpophalangeal1_L'].child =[['Fingers','Interphalangeal1_L']]
skeleton.segments['Fingers']['Metacarpophalangeal2_L'].child =[['Fingers','Interphalangeal2_L']]
skeleton.segments['Fingers']['Metacarpophalangeal3_L'].child =[['Fingers','Interphalangeal3_L']]
skeleton.segments['Fingers']['Metacarpophalangeal4_L'].child =[['Fingers','Interphalangeal4_L']]
skeleton.segments['Thigh']['Hip_L'].child = [['Leg','Knee_L']]
skeleton.segments['Leg']['Knee_L'].child = [['Foot','Ankle_L']]
skeleton.segments['Foot']['Ankle_L'].child = [['Foot','Intertarsal_L'],['Toes','Metatarsophalangeal1_L'],['Toes','Metatarsophalangeal2_L'],['Toes','Metatarsophalangeal3_L'],['Toes','Metatarsophalangeal4_L'],['Toes','Metatarsophalangeal5_L']]
skeleton.segments['Toes']['Metatarsophalangeal1_L'].child =[['Toes','Interphalangeal1_L']]
skeleton.segments['Toes']['Metatarsophalangeal2_L'].child =[['Toes','Interphalangeal2_L']]
skeleton.segments['Toes']['Metatarsophalangeal3_L'].child =[['Toes','Interphalangeal3_L']]
skeleton.segments['Toes']['Metatarsophalangeal4_L'].child =[['Toes','Interphalangeal4_L']]
skeleton.segments['Toes']['Metatarsophalangeal5_L'].child =[['Toes','Interphalangeal5_L']]
skeleton.segments['Shoulder']['Sternoclavicular_R'].child = [['Girdle','Acromioclavicular_R']]
skeleton.segments['Girdle']['Acromioclavicular_R'].child = [['Arm','Shoulder_R']]
skeleton.segments['Arm']['Shoulder_R'].child = [['Forearm','Elbow_R']] 
skeleton.segments['Forearm']['Elbow_R'].child = [['Forearm','Radioulnar_R']]
skeleton.segments['Forearm']['Radioulnar_R'].child = [['Hand','Wrist_R']]
skeleton.segments['Hand']['Wrist_R'].child = [['Thumb','Carpometacarpal_R'],['Fingers','Metacarpophalangeal1_R'],['Fingers','Metacarpophalangeal2_R'],['Fingers','Metacarpophalangeal3_R'],['Fingers','Metacarpophalangeal4_R']]
skeleton.segments['Thumb']['Carpometacarpal_R'].child = [['Thumb','Metacarpophalangeal_R']]
skeleton.segments['Thumb']['Metacarpophalangeal_R'].child = [['Thumb','Interphalangeal_R']]
skeleton.segments['Fingers']['Metacarpophalangeal1_R'].child =[['Fingers','Interphalangeal1_R']]
skeleton.segments['Fingers']['Metacarpophalangeal2_R'].child =[['Fingers','Interphalangeal2_R']]
skeleton.segments['Fingers']['Metacarpophalangeal3_R'].child =[['Fingers','Interphalangeal3_R']]
skeleton.segments['Fingers']['Metacarpophalangeal4_R'].child =[['Fingers','Interphalangeal4_R']]
skeleton.segments['Thigh']['Hip_R'].child = [['Leg','Knee_R']]
skeleton.segments['Leg']['Knee_R'].child = [['Foot','Ankle_R']]
skeleton.segments['Foot']['Ankle_R'].child = [['Foot','Intertarsal_R'],['Toes','Metatarsophalangeal1_R'],['Toes','Metatarsophalangeal2_R'],['Toes','Metatarsophalangeal3_R'],['Toes','Metatarsophalangeal4_R'],['Toes','Metatarsophalangeal5_R']]
skeleton.segments['Toes']['Metatarsophalangeal1_R'].child =[['Toes','Interphalangeal1_R']]
skeleton.segments['Toes']['Metatarsophalangeal2_R'].child =[['Toes','Interphalangeal2_R']]
skeleton.segments['Toes']['Metatarsophalangeal3_R'].child =[['Toes','Interphalangeal3_R']]
skeleton.segments['Toes']['Metatarsophalangeal4_R'].child =[['Toes','Interphalangeal4_R']]
skeleton.segments['Toes']['Metatarsophalangeal5_R'].child =[['Toes','Interphalangeal5_R']]

skeleton.addParents()

skeleton.segments['Trunk']['root'].addIMU(imu('/temp_4'))
skeleton.segments['Shoulder']['Sternoclavicular_L'].addIMU(imu('/l_shoulder'))
skeleton.segments['Shoulder']['Sternoclavicular_R'].addIMU(imu('/r_shoulder'))
skeleton.segments['Forearm']['Elbow_R'].addIMU(imu('/r_lower_arm'))
skeleton.segments['Arm']['Shoulder_R'].addIMU(imu('/r_upper_arm'))
skeleton.segments['Hand']['Wrist_R'].addIMU(imu('/r_hand')) 
skeleton.segments['Arm']['Shoulder_L'].addIMU(imu('/l_upper_arm'))
skeleton.segments['Forearm']['Elbow_L'].addIMU(imu('/l_lower_arm'))
skeleton.segments['Hand']['Wrist_L'].addIMU(imu('/l_hand')) 
skeleton.segments['Trunk']['Intervertebral3'].addIMU(imu('/chest'))
#skeleton.segments['Thigh']['Hip_R'].addIMU(imu('/temp_2'))
#skeleton.segments['Leg']['Knee_R'].addIMU(imu('/r_lower_leg'))
#skeleton.segments['Foot']['Ankle_R'].addIMU(imu('/r_foot'))
#skeleton.segments['Thigh']['Hip_L'].addIMU(imu('/l_upper_leg'))
#skeleton.segments['Leg']['Knee_L'].addIMU(imu('/l_lower_leg'))
#skeleton.segments['Foot']['Ankle_L'].addIMU(imu('/l_foot'))


#'temp_1',
#'temp_3'
#'temp_5'
#'temp_6'

#rospy.sleep(.1)
while not rospy.is_shutdown():
    r=rospy.Rate(60)
    r.sleep()
    skeleton.update()
