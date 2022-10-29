#pragma once

#include "software/geom/algorithms/acute_angle.h"
#include "software/geom/algorithms/intersection.h"
#include "software/geom/rectangle.h"
#include "software/geom/ray.h"
#include "software/geom/vector.h"

/**
 * Maps points to the edge of a rectangle
 * 
 * @param point1 one of the rectangle's corners
 * @param point2 the corner diagonally-opposite to point1
 * @param point3 the point to project onto the rectangle
 * 
 * @return The point at a rectangle edge projected from inputted point
 */
Point rectangleEdge(const Point &point1, const Point &point2, const Point &point3);

 

