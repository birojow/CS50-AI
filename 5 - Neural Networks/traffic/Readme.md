1st run:
Convolutional layer: 30 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 128, dropout 0.5;
Result: loss: 3.4998 - accuracy: 0.0567
Terrible result.

2nd run:
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.5;
Result: loss: 0.2956 - accuracy: 0.9285
Increased the filters from 30 to 100, and double the size of the hidden layer. The improvement is amazing. Time to run: 42ms/step.

3rd run
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 128, dropout 0.5;
Hidden layer: size 128, dropout 0.5;
Result: loss: 3.4977 - accuracy: 0.0561
Splitting one hidden layer of 256 into two of 128, I got almost the same result of the first run. It seems like the size of the hidden layers are more important than the number of layers. Unless I made a mistake in the syntax, and the second layer wasn't included.

4th run
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 128, dropout 0.5;
Hidden layer: size 128, dropout 0.5;
Hidden layer: size 128, dropout 0.5;
Hidden layer: size 128, dropout 0.5;
Result: loss: 3.5002 - accuracy: 0.0561
To check my theory from the last run, I doubled the number of hidden layers. No improvement at all.

5th run
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 512, dropout 0.5;
Result: loss: 0.2948 - accuracy: 0.9294
Still playing with hidden layers. Merged the four 128 sized hidden layers into one. Not a good result. Almost as good as the second run, but it took 80% more time to run (75ms/step).

6th run
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: 0.3155 - accuracy: 0.9373
Changed the size of the hidden layer back to 256 (which produced the best result so far), and the dropout from 0.5 to 0.3. Little improvement over the second run.

7th run
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.7;
Result: loss: 3.4967 - accuracy: 0.0567
Changed the dropout from 0.3 to 0.7. Terrible result again

8th run
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 3x3 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: 0.2669 - accuracy: 0.9359
Changed the dropout back to 0.3. Increased the pooling size to 3x3. No improvement.

9th run
Convolutional layer: 100 filters, 4x4 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: 0.3998 - accuracy: 0.9143
Changed the pooling size back to 2x2. Increased the kernel size to 4x4. No improvement.

10th run
Convolutional layer: 100 filters, 5x5 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: 0.2868 - accuracy: 0.9488
Increased the kernel to 5x5. Best result so far.

11th run
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Convolutional layer: 100 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: 0.2344 - accuracy: 0.9393
Added another set of convolutional and pooling layers. Kernel size back to 3x3. No improvement.

12th run
Convolutional layer: 256 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: loss: 0.3884 - accuracy: 0.9414
Back to one set of convolutional and pooling layers. Filters increased to 256. Best result so far, but with a considerably longer running time (112ms/step).

13th run
Convolutional layer: 128 filters, 3x3 kernel;
Pooling layer: 2x2 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: loss: 0.4657 - accuracy: 0.9113
Filters decreased to 128.

14th run
Convolutional layer: 100 filters, 5x5 kernel;
Pooling layer: 3x3 pool size;
Convolutional layer: 100 filters, 5x5 kernel;
Pooling layer: 3x3 pool size;
Hidden layer: size 256, dropout 0.3;
Result: loss: loss: 0.2228 - accuracy: 0.9503
Best result so far, with lower running time (22ms/step). I'm satisfied with that.

Conclusion: increasing the filters and the size of the hidden layer improved the accuracy, but only to a certain extent. Extra hidden layers didn't improved the accuracy. Extra convolutional and pooling layers only improved the result with bigger kernels and pooling sizes.