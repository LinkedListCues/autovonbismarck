using System;

namespace EECS214Assignment1
{
    public class QueueException : Exception
    {
        public QueueException(string message)
            : base(message)
        { }
    }

    public class QueueEmptyException : QueueException
    {
        public QueueEmptyException()
            : base("Attempt to dequeue from an empty queue")
        { }
    }

    public class QueueFullException : QueueException
    {
        public QueueFullException()
            : base("Attempt to enqueue to a full queue")
        { }
    }
}
