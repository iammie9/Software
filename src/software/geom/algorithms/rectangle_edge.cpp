#include "software/geom/algorithms/rectangle_edge.h"

Point rectangleEdge(const Point &point1, const Point &point2, const Point &point3)
{
    //creates a ray going from point3 towards the top corner of the rectangle
    explicit ray1 = Ray(point3, Vector(point1.x()-point3.x(),point1.y()-point3.y()));

    //the angle mainRay will take to rectangle
    Angle angle = ray1.getdiredction() + acuteAngle(point1, point2, point3) / 2; 

    //creates rectangle of interest
    explicit rectangle = rectangle(point1,point2);

    //ray to intersect with rectangle edge
    explicit mainRay = (point3, angle);

    
} 

