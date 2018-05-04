using System;
using System.IO;

namespace EECS214Assignment1
{
    /// <summary>
    /// A queue internally implemented as an array
    /// </summary>
    public class ArrayQueue : Queue
    {
        /// <summary>
        object[] theArray = new object[256];
        private int head;
        private int tail = 0;
        private int numElements = 0;

        /// Add object to end of queue
        /// </summary>
        /// <param name="o">object to add</param>
        public override void Enqueue(object o)
        {

            if (numElements == 256)
                throw new QueueFullException();

            theArray[tail] = o;
            if (tail == 255)
                tail = 0;
            else
            {
                tail = (tail + 1);
            }
            numElements = (numElements + 1);

        }

        /// <summary>
        /// Remove object from beginning of queue.
        /// </summary>
        /// <returns>Object at beginning of queue</returns>
        public override object Dequeue()
        {
            if (numElements == 0)
                throw new QueueEmptyException();

            if (head == 255)
                head = 0;
            else
            {
                head = (head + 1);
            }
            numElements = (numElements - 1);
            return theArray[head - 1];
        }

        /// <summary>
        /// The number of elements in the queue.
        /// </summary>
        public override int Count
        {
            get
            {
                return numElements;

            }
        }

        /// <summary>
        /// True if the queue is full and enqueuing of new elements is forbidden.
        /// </summary>
        public override bool IsFull
        {
            get
            {
                if (numElements == 256)
                    return true;
                else
                {
                    return false;
                }
            }
        }
    }
}
