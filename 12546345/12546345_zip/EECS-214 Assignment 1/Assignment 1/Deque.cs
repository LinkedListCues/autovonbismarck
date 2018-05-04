using System;

namespace EECS214Assignment1
{
    /// <summary>
    /// A double-ended queue
    /// Implement this as a doubly-linked list
    /// </summary>
    public class Deque
    {
        /// <summary>
        /// 
        class LinkedListCell
        {
            public object value;
            public LinkedListCell prev;
            public LinkedListCell next;
        }

        private LinkedListCell cell;
        private LinkedListCell first;
        private LinkedListCell last;

        private object theHold;

        private int numElements = 0;
        /// Add object to front of queue
        /// </summary>
        /// <param name="o">object to add</param>
        public void AddFront(object o)
        {

            cell = new LinkedListCell()
            {
                value = o,
                next = first,
                prev = null
            };
            numElements = (numElements + 1);

            if (numElements == 1)
            {
                first = cell;
                last = cell;
            }
            else
            {
                first.prev = cell;
                first = cell;
            }

            // TODO: Replace this line with your code.
            ///throw new NotImplementedException();
        }

        /// <summary>
        /// Remove object from beginning of queue.
        /// </summary>
        /// <returns>Object at beginning of queue</returns>
        public object RemoveFront()
        {

            if (numElements == 0)
                throw new QueueEmptyException();
            theHold = first.value;
            if (numElements == 1)
            {
                first = null;
                last = null;
            }
            else
            {
                first = first.next;
            }

            numElements = (numElements - 1);
            return theHold;
            // TODO: Replace this line with your code.
            ///throw new NotImplementedException();
        }

        /// <summary>
        /// Add object to end of queue
        /// </summary>
        /// <param name="o">object to add</param>
        public void AddEnd(object o)
        {
            cell = new LinkedListCell()
            {
                value = o,
                next = null,
                prev = last
            };
            numElements = (numElements + 1);

            if (numElements == 1)
            {
                first = cell;
                last = cell;
            }
            else
            {
                last.next = cell;
                last = cell;
            }

            // TODO: Replace this line with your code.
            ///throw new NotImplementedException();
        }

        /// <summary>
        /// Remove object from end of queue.
        /// </summary>
        /// <returns>Object at end of queue</returns>
        public object RemoveEnd()
        {
            if (numElements == 0)
                throw new QueueEmptyException();
            theHold = last.value;

            if (numElements == 1)
            {
                first = null;
                last = null;
            }
            else
            {
                last = last.prev;
            }

            numElements = (numElements - 1);
            return theHold;

            // TODO: Replace this line with your code.
            ///throw new NotImplementedException();
        }

        /// <summary>
        /// The number of elements in the queue.
        /// </summary>
        public int Count
        {
            get
            {
                return numElements;
                // TODO: Replace this line with your code.
                ///throw new NotImplementedException();
            }
        }

        /// <summary>
        /// True if the queue is empty and dequeuing is forbidden.
        /// </summary>
        public bool IsEmpty => Count == 0;
    }
}
