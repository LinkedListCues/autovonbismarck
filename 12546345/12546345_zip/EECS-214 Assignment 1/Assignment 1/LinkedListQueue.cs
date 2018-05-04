using System;
using System.Security.Policy;

namespace EECS214Assignment1
{
    /// <summary>
    /// A queue internally implemented as a linked list of objects
    /// </summary>
    public class LinkedListQueue : Queue
    {
        /// <summary>
        /// 
        class LinkedListCell
        {
            public object value;
            public LinkedListCell next;
        }

        private LinkedListCell cell;
        private LinkedListCell first;
        private LinkedListCell last;

        private object holder;

        private int numElements = 0;

        /// Add object to end of queue
        /// </summary>
        /// <param name="o">object to add</param>
        public override void Enqueue(object o)
        {
         
            cell = new LinkedListCell()
            {
                value = o,
                next = null
            };
            numElements = (numElements + 1);

            if (numElements == 1)
            {
                first = cell;
                last = first;
            }
        

            else

            {
                last.next = cell;
                last = cell;
            }

        }

        /// <summary>
        /// Remove object from beginning of queue.
        /// </summary>
        /// <returns>Object at beginning of queue</returns>
        public override object Dequeue()
        {
            if (numElements == 0)
                throw new QueueEmptyException();
            if (first == last)
            {
                holder = first.value;
                first = null;
                last = null;
                numElements = (numElements - 1);
                return holder;
            }

            holder = first.value;
            first = first.next;
            numElements = (numElements - 1);
            return holder;
 
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
        /// Note: LinkedListQueues can be grown to arbitrary length, and so can
        /// NEVER fill.
        /// </summary>
        public override bool IsFull
        {
            get
            {
                return false;

            }
        }
    }
}
