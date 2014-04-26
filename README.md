About 
=====

Hey, this is a program to calculate the minimum of any given real
function(well, there's a catch =|) through a GA (Genetic Algorithm) approach.

License 
=======

https://www.tldrlegal.com/l/gpl2

You may copy, distribute and modify the software as long as you track 
changes/dates of in source files and keep all modifications under GPL. 
You can distribute your application using a GPL library commercially, 
but you must also disclose the source code.

Prerequisites
=============

I recommend using *ipython* as your console, and start it with the --pylab
command line argument. But if you don't like it, all that is required in order 
to run this is *numpy* and *BitStream*. They are fairly well known libraries 
and you probably already have them.

Usage 
=====

First, you should probably instantiate a new Environment(). It starts with a
predefined target function that you can just run to get the feeling of how 
things work.

    Example:

    e = Environment()

    e.fast_foward()

Details 
=======

I tried to keep the code clean and simple with a lot of one-liners so it
wouldn't be so daunting to read like other similar codes. The basic idea
is this:

    1.  First create a random population. 

    2.  Select another population of the same size but through a roulette 
        method. 

        2.1 The roulette method tries to compute something I called 
            *population fitness* which is just the sum of the fitness of the 
            entire population. Then the probability of selecting any 
            individual in the roulette is given by it's fitness divided by the
            population fitness. If the target function is such that it's 
            maximum value is higher than 4000 you should set the environment 
            normalizing factor that is used to get over the problem of 
            calculating proportions between positive and negative numbers 

    3.  Couple all selected parents. Unfortunately this requires that your 
        population number is even.

    4.  Crossover the selected pairs. 

    5.  For each individual produced so far, try to mutate it. 

    6. This new batch will be your population for the next iteration.

TL;DR 
=====

* Population size must be an even number. It won't work if your function have
* A higher value than 4000 in the specified range, unless you set the upperbound parameter when creating the Environment.

Author 
======

github.com/hoarf 
matehackers.org
