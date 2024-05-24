import numpy as np
import pygame
import Ball


def SignedAngle(vec1):
    if np.linalg.norm(vec1) == 0:
        return 0
    vec1 = np.array(vec1)
    vec1 = vec1 / np.linalg.norm(vec1)
    X_vec = np.array((1, 0))
    Y_vec = np.array((0, 1))
    dot1 = np.dot(vec1, X_vec)
    dot2 = np.dot(vec1, Y_vec)

    angle = (((dot2 > 0) * 2 - 1) * np.arccos(dot1)) / np.pi * 180.0
    if(angle<0):
        angle = 360+angle
    return angle

def LineIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       #raise Exception('lines do not intersect')
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def SegmentIntersection(A, B, C, D):
    intersection = LineIntersection((A, B), (C, D))
    if(intersection == False):
        return False, np.array((0, 0))

    v1 = B-A
    v2 = D-C

    if 1>=np.dot((intersection - A)/np.linalg.norm(v1), v1/np.linalg.norm(v1))>=0 and 1>=np.dot((intersection - C)/np.linalg.norm(v2), v2/np.linalg.norm(v2))>=0:
        return True, intersection
    else:
        return False, np.array((0, 0))

class ConvexPolygon:
    def __init__(self, *points, fixed = False, fixed_rotation = False, move_center_of_mass = (0, 0), mass_per_area = 1.0):
        self.fixed_in_space = fixed
        self.fixed_rotation = fixed_rotation
        self.points = list(points)
        self.center = np.array([0, 0])
        for i in range(len(self.points)):
            self.points[i] = np.array(self.points[i])
        self.originalpoints = self.points[:]
        self.center_of_mass = np.array((0, 0))
        self.CreateConvexHull()
        self.mean_point = sum(self.points) / len(self.points)
        self.area = 0
        self.FindCenterOfMass()
        self.center_of_mass+=np.array(move_center_of_mass)

        for i in range(len(self.points)):
            self.points[i] = self.points[i] - self.center_of_mass
        for i in range(len(self.originalpoints)):
            self.originalpoints[i] = self.originalpoints[i] - self.center_of_mass
        self.mean_point = self.mean_point - self.center_of_mass
        self.center_of_mass = self.center_of_mass - self.center_of_mass

        self.true_position = self.center_of_mass

        self.mass_per_area = mass_per_area
        self.rotational_inertia = 0

        self.SetRotationalInertia()

        self.velocity = np.array((0, 0))
        self.rotation = 0
        self.rotational_velocity = 0 #in radians/s

        self.simple_radius = 0
        self.FindSimpleRadius()

        self.latest_pos = np.array((self.center_of_mass))
        self.latest_rotation = self.rotation
        self.displacement = np.array((0, 0))
        self.angular_displacement = 0

    def CreateConvexHull(self):
        points = self.points[:]
        points.sort(key=lambda x: x[1])
        lowest = points[0]
        points = points[1:]
        points.sort(key=lambda x: SignedAngle(x - lowest))

        stack = [lowest, points[0]]
        i = 1
        while i < len(points):
            vec1 = stack[-1] - stack[-2]
            vec2 = points[i] - stack[-1]
            rotated_vec1 = np.array((-vec1[1], vec1[0]))
            while (np.dot(vec2, rotated_vec1) <= 0 and len(stack) > 2):
                stack.pop(-1)
                vec1 = stack[-1] - stack[-2]
                vec2 = points[i] - stack[-1]
                rotated_vec1 = np.array((-vec1[1], vec1[0]))
            stack.append(points[i])
            i += 1
        self.points = stack[:]

    def DisplayPoints(self, screen):
        connect = True
        for point in self.points:
            pygame.draw.circle(screen, (255, 0, 0), point, 5)
        if connect:
            for point in range(len(self.points)):
                pygame.draw.line(screen, (255, 0, 0), self.points[point],self.points[(point+1)%len(self.points)],  5)
        self.ShowMeanPoint(screen)
        self.ShowCenterOfMass(screen)

    def DisplayAllPoints(self, screen):
        for point in self.originalpoints:
            pygame.draw.circle(screen, (255, 0, 0), point, 5)
        self.ShowMeanPoint(screen)
        self.ShowCenterOfMass(screen)

    def ShowMeanPoint(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), self.mean_point, 5)

    def ShowCenterOfMass(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.center_of_mass, 5)

    def FindCenterOfMass(self):
        points = self.points[:]
        points.sort(key = lambda x : (x[1], x[0]))
        center = np.array((0, 0))
        area = 0
        for i in range(0, len(points) - 2):
            triangle_center_of_mass = (points[i] + points[i + 1] + points[i + 2]) / 3.0
            triangle_area = (1.0 / 2.0) * abs(
                    points[i + 0][0] * (points[i + 1][1] - points[i + 2][1]) +
                    points[i + 1][0] * (points[i + 2][1] - points[i + 0][1]) +
                    points[i + 2][0] * (points[i + 0][1] - points[i + 1][1]))

            center = center + triangle_center_of_mass*triangle_area
            area = area + triangle_area

        self.center_of_mass = center/area
        #print(self.center_of_mass)
        self.area = area
    def Translate(self, translation):
        translation = np.array(translation)
        self.true_position = self.true_position + translation
        for i in range(len(self.points)):
            self.points[i] = self.points[i] + translation
        for i in range(len(self.originalpoints)):
            self.originalpoints[i] = self.originalpoints[i] + translation
        self.mean_point = self.mean_point + translation
        self.center_of_mass = self.center_of_mass + translation

    def Rotate(self, rotation, rotationpoint = None):
        if rotationpoint == None:
            rotationpoint = pygame.Vector2(self.center_of_mass[0], self.center_of_mass[1])
        else:
            rotationpoint = pygame.Vector2(rotationpoint)
        self.rotation+=rotation
        matrix = np.array(((np.cos(rotation), -np.sin(rotation)), (np.sin(rotation), np.cos(rotation))))
        for i in range(len(self.points)):
            self.points[i] = self.points[i] - rotationpoint
            self.points[i] = matrix.dot(self.points[i])
            self.points[i] = self.points[i] + rotationpoint
        for i in range(len(self.originalpoints)):
            self.originalpoints[i] = self.originalpoints[i] - rotationpoint
            self.originalpoints[i] = matrix.dot(self.originalpoints[i])
            self.originalpoints[i] = self.originalpoints[i] + rotationpoint
        self.mean_point = self.mean_point-rotationpoint
        self.mean_point = matrix.dot(self.mean_point)
        self.mean_point = self.mean_point + rotationpoint
    def GoTo(self, position):
        translation = position - self.center_of_mass
        self.true_position = self.true_position + translation
        for i in range(len(self.points)):
            self.points[i] = self.points[i] + translation
        for i in range(len(self.originalpoints)):
            self.originalpoints[i] = self.originalpoints[i] + translation
        self.mean_point = self.mean_point + translation
        self.center_of_mass = self.center_of_mass + translation
    def SetRotationalInertia(self):
        self.points.sort(key = lambda x : x[1])
        for i in range(len(self.points)-2):
            point1 = self.points[i]
            point2 = self.points[i+1]
            point3 = self.points[i+2]

            u = point2 - point1
            v = point3 - point1
            I = (self.mass_per_area * np.linalg.norm(np.cross(u, v)) / 12.0) * (np.linalg.norm(u)+np.linalg.norm(v) + np.dot(u, v))

            m = self.mass_per_area * (1.0/2.0) * abs(point1[0] * (point2[1] - point3[1]) + point2[0] * (point3[1] - point1[1]) + point3[0] * (point1[1] - point2[1]))

            self.rotational_inertia += I + m * np.linalg.norm(self.center_of_mass - (point1 + point2 + point3)/3.0)**2
    def FindSimpleRadius(self):
        max = 0
        for point in self.points:
            if np.linalg.norm(point - self.center_of_mass) > max:
                max = np.linalg.norm(point - self.center_of_mass)
        self.simple_radius = max
    def MoveCenterOfMass(self, offset : tuple):
        offset = np.array(offset)
        self.center_of_mass+=offset
        self.SetRotationalInertia()

class PhysicsEngine:
    def __init__(self):
        self.convex_polygons = []
        self.balls = []

    def FindAndSolvePolygonsCollision(self, pol1 : ConvexPolygon, pol2 : ConvexPolygon):
        #DIAGONALS THEOREM
        minp1 = min(pol1.points, key = lambda x : x[1])
        minp2 = min(pol2.points, key=lambda x: x[1])
        pol1.points.sort(key = lambda x : SignedAngle(x - minp1))
        pol2.points.sort(key=lambda x: SignedAngle(x - minp2))

        offset_coeff = 2.0

        for i in range(len(pol1.points)):
            p1 = pol1.points[i]
            p2 = pol1.points[(i + 1)%len(pol1.points)]

            for j in range(len(pol2.points)):
                intersection = SegmentIntersection(p1, p2, pol2.points[j], pol2.center_of_mass)
                if intersection[0] == True:
                    intersection = intersection[1]
                    vec = intersection - pol2.points[j]
                    if pol1.fixed_in_space == True and pol2.fixed_in_space == True:
                        continue
                    if pol1.fixed_in_space == False and pol2.fixed_in_space == False:
                        pol1.Translate(-offset_coeff/2.0 * (vec))
                        pol2.Translate(offset_coeff/2.0 * (vec))
                    elif pol1.fixed_in_space == True:
                        pol2.Translate(offset_coeff * (vec))
                    elif pol2.fixed_in_space == True:
                        pol1.Translate(-offset_coeff * (vec))
                    normal = (p2-p1)
                    normal = np.array((normal[1], -normal[0]))
                    normal = normal/np.linalg.norm(normal)
                    self.ComputeCollisionResponse(pol1, pol2, intersection, normal)

        for i in range(len(pol2.points)):
            p1 = pol2.points[i]
            p2 = pol2.points[(i + 1)%len(pol2.points)]

            for j in range(len(pol1.points)):
                intersection = SegmentIntersection(p1, p2, pol1.points[j], pol1.center_of_mass)
                if intersection[0] == True:
                    intersection = intersection[1]
                    vec = intersection - pol1.points[j]
                    if pol1.fixed_in_space == True and pol2.fixed_in_space == True:
                        continue
                    if pol1.fixed_in_space == False and pol2.fixed_in_space == False:
                        pol2.Translate(-offset_coeff/2.0 * (vec))
                        pol1.Translate(offset_coeff/2.0 * (vec))
                    elif pol1.fixed_in_space == True:
                        pol2.Translate(-offset_coeff * (vec))
                    elif pol2.fixed_in_space == True:
                        pol1.Translate(offset_coeff * (vec))
                    normal = (p2 - p1)
                    normal = np.array((normal[1], -normal[0]))
                    normal = normal / np.linalg.norm(normal)
                    self.ComputeCollisionResponse(pol1, pol2, intersection, normal)
        #SEPARATE AXIS THEOREM
        '''minp1 = min(pol1.points, key=lambda x: x[1])
        minp2 = min(pol2.points, key=lambda x: x[1])
        pol1.points.sort(key=lambda x: SignedAngle(x - minp1))
        pol2.points.sort(key=lambda x: SignedAngle(x - minp2))
        #pol1 axis
        for i in range(len(pol1.points)):
            vec = pol1.points[(i+1)%len(pol1.points)] - pol1.points[i]
            vec = np.array(vec[1], vec[0])
            max1 = 0
            min1 = 0

            max2 = np.dot((pol2.points[0] - pol1.points[i]), vec)
            min2 = np.dot((pol2.points[0] - pol1.points[i]), vec)
            for a in range(len(pol1.points)):
                if np.dot((pol1.points[a] - pol1.points[i]), vec)<min1:
                    min1 = np.dot((pol1.points[a] - pol1.points[i]), vec)
            for b in range(len(pol2.points)):
                if np.dot((pol2.points[b] - pol1.points[i]), vec) < min2:
                    min2 = np.dot((pol2.points[b] - pol1.points[i]), vec)
                if np.dot((pol2.points[b] - pol1.points[i]), vec)>max2:
                    min1 = np.dot((pol2.points[b] - pol1.points[i]), vec)

            if max1 > max2 and min1 > max2:
                pass'''


    def ComputeCollisionResponse(self, p1 : ConvexPolygon, p2 : ConvexPolygon, intersection, normal):
        e = 1.0
        ap = intersection - p1.center_of_mass
        bp = intersection - p2.center_of_mass
        v_ab = (p1.velocity + p1.rotational_velocity * np.array((-ap[1], ap[0]))) - (p2.velocity + p2.rotational_velocity * np.array((-bp[1], bp[0])))
        j = -(1.0 + e) * np.dot(v_ab, normal)
        inverse_masses = 1.0 / (p1.mass_per_area * p1.area) + 1.0 / (p2.mass_per_area * p2.area)
        if p1.fixed_in_space == True:
            inverse_masses = 1.0 / (p2.mass_per_area * p2.area)
            j = j / (inverse_masses + (np.dot(np.array((-bp[1], bp[0])), normal)**2 / p2.rotational_inertia))
            p2.velocity = p2.velocity - normal * j / (p2.mass_per_area * p2.area)
            p2.rotational_velocity = p2.rotational_velocity - np.dot(np.array((-bp[1], bp[0])), normal) * j / p2.rotational_inertia
        elif p2.fixed_in_space == True:
            inverse_masses = 1.0 / (p1.mass_per_area * p1.area)
            j = j / (inverse_masses + (np.dot(np.array((-ap[1], ap[0])), normal)**2 / p1.rotational_inertia))
            p1.velocity = p1.velocity + normal * j / (p1.mass_per_area * p1.area)
            p1.rotational_velocity = p1.rotational_velocity + np.dot(np.array((-ap[1], ap[0])), normal) * j / p1.rotational_inertia
        else:
            j = j / (inverse_masses + (np.dot(np.array((-ap[1], ap[0])), normal)**2 / p1.rotational_inertia) + (np.dot(np.array((-bp[1], bp[0])), normal)**2 / p2.rotational_inertia))
            p1.velocity = p1.velocity + normal * j / (p1.mass_per_area * p1.area)
            p2.velocity = p2.velocity - normal * j / (p2.mass_per_area * p2.area)

            p1.rotational_velocity = p1.rotational_velocity + np.dot(np.array((-ap[1], ap[0])), normal) * j / p1.rotational_inertia
            p2.rotational_velocity = p2.rotational_velocity - np.dot(np.array((-bp[1], bp[0])), normal) * j / p2.rotational_inertia

    def FindAndSolveCollisionBetweenBallAndPolygon(self, ball : Ball, polygon : ConvexPolygon):
        collision = np.array((0, 0))
        normal = np.array((0, 0))
        for i in range(len(polygon.points)):
            A = polygon.points[i]
            B = polygon.points[(i+1)%len(polygon.points)]
            C = ball.position
            xA = polygon.points[i][0]
            yA = polygon.points[i][1]

            xB = polygon.points[(i+1)%len(polygon.points)][0]
            yB = polygon.points[(i+1)%len(polygon.points)][1]

            xC = ball.position[0]
            yC = ball.position[1]
            D = (np.abs((xB-xA)*(yC-yA) - (yB-yA)*(xC-xA)))/np.sqrt((xB-xA)**2 + (yB-yA)**2)
            if np.dot(A-B, C-B)>0 and np.dot(B-A, C - A)>0:
                if D<ball.radius:
                    coeff = ((xB-xA)*(xC-xA) + (yB-yA)*(yC-yA))/((xB-xA)**2 + (yB-yA)**2)
                    collision[0] = xA + (xB-xA) * coeff
                    collision[1] = yA + (yB - yA) * coeff
                    normal = (ball.position-collision)
                    normal = normal/np.linalg.norm(normal)
                    ball.position = ball.position + normal*(ball.radius-D)*3
                    return True, collision, normal
        for i in range(len(polygon.points)):
            A = polygon.points[i]
            B = polygon.points[(i + 1) % len(polygon.points)]
            C = ball.position
            xA = polygon.points[i][0]
            yA = polygon.points[i][1]

            xB = polygon.points[(i + 1) % len(polygon.points)][0]
            yB = polygon.points[(i + 1) % len(polygon.points)][1]

            xC = ball.position[0]
            yC = ball.position[1]
            D = (np.abs((xB - xA) * (yC - yA) - (yB - yA) * (xC - xA))) / np.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
            if not(np.dot(A-B, C-B)>0 and np.dot(B-A, C - A)>0):
                D = min(np.linalg.norm(A-C), np.linalg.norm(B-C))
                if D<ball.radius:
                    if D==np.linalg.norm(A-C):
                        collision = A
                    else:
                        collision = B
                    normal = (ball.position-collision)
                    normal = normal/np.linalg.norm(normal)
                    ball.position = ball.position + normal*(ball.radius-np.linalg.norm(ball.position-collision))*3
                    return True, collision, normal
        return False, collision, normal
    def FindAndSolveCollisionBetweenBallAndBall(self, b1 : Ball, b2 : Ball):
        if b1.radius + b2.radius > np.linalg.norm(b1.position - b2.position):
            dif = b1.radius + b2.radius - np.linalg.norm(b1.position - b2.position)
            normal = (b2.position - b1.position)/np.linalg.norm(b1.position - b2.position)
            if not b1.fixed_in_space:
                b1.position = b1.position - normal*dif*(b1.radius/(b1.radius + b2.radius))
                b2.score+=10
            if not b2.fixed_in_space:
                b2.position = b2.position + normal * dif * (b2.radius / (b1.radius + b2.radius))
                b1.score+=10
            return True, b1.position + normal, normal
        else:
            return False, np.array((0, 0)), np.array((0, 0))

    def ComputeCollisionResponseBetweenBallAndBall(self, b1 : Ball, b2 : Ball, collision : np.array, normal : np.array):
        e = 1.0
        v_ab = (b1.velocity - b2.velocity)
        m1 = b1.area * b1.mass_per_area
        m2 = b2.area * b2.mass_per_area
        inverse_masses = 1.0/m1 + 1.0/m2
        if b1.fixed_in_space:
            b2.velocity = b2.velocity - (-(1+e) * np.dot(v_ab, normal)/(inverse_masses))/m1*normal
        elif b2.fixed_in_space:
            b1.velocity = b1.velocity + (-(1 + e) * np.dot(v_ab, normal) / (inverse_masses)) / m2 * normal
        else:
            b2.velocity = b2.velocity - (-(1+e) * np.dot(v_ab, normal)/(inverse_masses))/m1*normal
            b1.velocity = b1.velocity + (-(1 + e) * np.dot(v_ab, normal) / (inverse_masses)) / m2 * normal




    def ComputeCollisionResponseBetweenBallAndPolygon(self, ball : Ball, polygon : ConvexPolygon, collision : np.array, normal : np.array):
        e = 1.0
        ap = collision - ball.position
        bp = collision - polygon.center_of_mass
        #v_ab = (ball.velocity + ball.rotational_velocity * np.array((-ap[1], ap[0]))) - (polygon.velocity + polygon.rotational_velocity * np.array((-bp[1], bp[0])) )
        v_ab = (ball.velocity) - (polygon.velocity + polygon.rotational_velocity * np.array((-bp[1], bp[0])))
        j = -(1.0 + e) * np.dot(v_ab, normal)
        inverse_masses = 1.0 / (ball.mass_per_area * ball.area) + 1.0 / (polygon.mass_per_area * polygon.area)
        if ball.fixed_in_space == True:
            inverse_masses = 1.0 / (polygon.mass_per_area * polygon.area) + (1.0 / (ball.mass_per_area * ball.area))
            j = j / (inverse_masses + (np.dot(np.array((-bp[1], bp[0])), normal) ** 2 / polygon.rotational_inertia))
            polygon.velocity = polygon.velocity - normal * j / (polygon.mass_per_area * polygon.area)
            polygon.rotational_velocity = polygon.rotational_velocity - np.dot(np.array((-bp[1], bp[0])),
                                                                               normal) * j / polygon.rotational_inertia
        elif polygon.fixed_in_space == True and polygon.fixed_rotation == True:
            #print("hey")
            '''
            inverse_masses = 1.0 / (ball.mass_per_area * ball.area)+1.0 / (polygon.mass_per_area * polygon.area)
            j = j / (inverse_masses + (np.dot(np.array((-ap[1], ap[0])), normal) ** 2 / ball.rotational_inertia) + (
                    np.dot(np.array((-bp[1], bp[0])), normal) ** 2 / polygon.rotational_inertia))
            '''
            v_pol = polygon.rotational_velocity * np.array((-bp[1], bp[0]))

            #ball.velocity = ball.velocity + normal * j / (ball.mass_per_area * ball.area)
            m1 = ball.mass_per_area * ball.area
            m2 = polygon.area * polygon.mass_per_area
            #ball.velocity = (ball.velocity*m1 + v_pol * m2 - (ball.velocity - v_pol)/(m2)) / (m1+m2)
            ball.velocity = ball.velocity + (-(1+e) * np.dot(v_ab, normal)/(inverse_masses))/m1*normal * 1.1
            #ball.rotational_velocity = ball.rotational_velocity + np.dot(np.array((-ap[1], ap[0])),normal) * j / ball.rotational_inertia
        else:
            j = j / (inverse_masses + (np.dot(np.array((-ap[1], ap[0])), normal) ** 2 / ball.rotational_inertia) + (
                    np.dot(np.array((-bp[1], bp[0])), normal) ** 2 / polygon.rotational_inertia))
            ball.velocity = ball.velocity + normal * j / (ball.mass_per_area * ball.area)
            polygon.velocity = polygon.velocity - normal * j / (polygon.mass_per_area * polygon.area)

            ball.rotational_velocity = ball.rotational_velocity + np.dot(np.array((-ap[1], ap[0])),
                                                                         normal) * j / ball.rotational_inertia
            polygon.rotational_velocity = polygon.rotational_velocity - np.dot(np.array((-bp[1], bp[0])),
                                                                               normal) * j / polygon.rotational_inertia


    def clear(self):
        self.convex_polygons.clear()
        self.balls.clear()


    def Update(self, screen, delta_time):

        for i in range(len(self.convex_polygons)):
            self.convex_polygons[i].displacement = (np.array(self.convex_polygons[i].center_of_mass) - np.array(self.convex_polygons[i].latest_pos))*60
            self.convex_polygons[i].angular_displacement = (self.convex_polygons[i].rotation - self.convex_polygons[i].latest_rotation)*60
            self.convex_polygons[i].latest_pos = self.convex_polygons[i].center_of_mass
            self.convex_polygons[i].latest_rotation = self.convex_polygons[i].rotation
            '''
            for j in range(i+1, len(self.convex_polygons)):
                if i == j:
                    continue
                if np.linalg.norm(self.convex_polygons[i].center_of_mass - self.convex_polygons[j].center_of_mass)<=(self.convex_polygons[i].simple_radius + self.convex_polygons[j].simple_radius):
                    self.FindAndSolvePolygonsCollision(self.convex_polygons[i], self.convex_polygons[j])
            '''
            for j in range(len(self.balls)):
                compute = self.FindAndSolveCollisionBetweenBallAndPolygon(self.balls[j], self.convex_polygons[i])
                if compute[0] == True:
                    self.ComputeCollisionResponseBetweenBallAndPolygon(self.balls[j], self.convex_polygons[i], compute[1], compute[2])
        for i in range(len(self.balls)):
            for j in range(i+1, len(self.balls)):
                if i==j:
                    continue
                compute = self.FindAndSolveCollisionBetweenBallAndBall(self.balls[i], self.balls[j])
                if compute[0] == True:
                    self.ComputeCollisionResponseBetweenBallAndBall(self.balls[i], self.balls[j], compute[1], compute[2])
        for i in range(len(self.convex_polygons)):
            if self.convex_polygons[i].fixed_in_space == False:
                self.convex_polygons[i].velocity = self.convex_polygons[i].velocity + np.array((0, 9.81*20))*delta_time
                self.convex_polygons[i].velocity*=(0.999)
                self.convex_polygons[i].Translate(self.convex_polygons[i].velocity*delta_time)
            if self.convex_polygons[i].fixed_rotation == False:
                self.convex_polygons[i].Rotate(self.convex_polygons[i].rotational_velocity*delta_time)
                self.convex_polygons[i].rotational_velocity *= (0.999)


            #self.convex_polygons[i].DisplayPoints(screen)
        for i in range(len(self.balls)):
            if not self.balls[i].fixed_in_space:
                self.balls[i].velocity = self.balls[i].velocity + np.array((0, 9.81*40))*delta_time
                self.balls[i].position = self.balls[i].position + self.balls[i].velocity * delta_time
                self.balls[i].velocity *= (0.999)
            #self.balls[i].Display(screen)
