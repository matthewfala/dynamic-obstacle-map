# DOM -- Dynamic Obstacle Map
## by Matthew J.W. Fala


# Notes
- KOrderMath by Kishore Venkateshan

_____

# Documentation

############################################
#       DOM (Dynamic Obstacle Map)         #
#       By Matthew J.W. Fala               #
############################################

# Description: The DOM (Dynamic Obstacle Map) was written for USC AUV by Matthew J.W. Fala.
# It consolidates all Computer Vision Obstacle discoveries and dynamically generates a probability map.
# Objects that have a high threshold probability of existence are logged to a FOM or Fixed Obstacle Map on
# the client side.

# Python Interface
 Call update_actors to update the world

# ROS Interface (Needs Implementation)
#
# Interface: The interface is ROS Message.
> ROS Topic: /fom

# Message Parameters:
>   string cmd
>   string type
>   int id
>   float64 x
>   float64 y
>   float64 z

# Continuation:

##########################################################################
# OBSTACLES
##########################################################################
- Gate
- Dice Buoy
- Chip Dispenser
- Slot Machine
- Roulette
- Cashier Bins
