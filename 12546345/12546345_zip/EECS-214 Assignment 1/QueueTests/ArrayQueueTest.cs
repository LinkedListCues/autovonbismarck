using EECS214Assignment1;
using Microsoft.VisualStudio.TestTools.UnitTesting;
namespace QueueTests
{
    /// <summary>
    ///This is a test class for ArrayQueueTest and is intended
    ///to contain all ArrayQueueTest Unit Tests
    ///</summary>
    [TestClass()]
    public class ArrayQueueTest
    {
        [TestMethod()]
        public void ConstructorCreatesEmptyQueueTest()
        {
            ArrayQueue target = new ArrayQueue();
            Assert.IsTrue(target.IsEmpty, "A newly created ArrayQueue should have IsEmpty=true, but doesn't");
        }

        [TestMethod()]
        public void ConstructorCreatesNonFullQueueTest()
        {
            ArrayQueue target = new ArrayQueue();
            Assert.IsFalse(target.IsFull, "A newly created ArrayQueue should have IsFull=false, but doesn't");
        }

        [TestMethod()]
        [ExpectedException(typeof(QueueFullException), "Adding to full queue should throw QueueFullException")]
        public void EnqueueToFullQueueThrowsQueueFullExceptionTest()
        {
            ArrayQueue target = new ArrayQueue();
            Assert.IsFalse(target.IsFull);
            int i;
            for (i = 0; i < 1000000 && !target.IsFull; i++)
                target.Enqueue(i);
            Assert.IsTrue(target.IsFull, "Added 1000000 elements to ArrayQueue and it still doesn't return IsFull=true");
            target.Enqueue(0);
            Assert.Fail("Enqueue to full queue didn't throw QueueEmptyException");
        }

        /// <summary>
        ///A test for Count
        ///</summary>
        [TestMethod()]
        public void CountTest()
        {
            ArrayQueue target = new ArrayQueue();
            for (int i = 0; i < 1000000 && !target.IsFull; i++)
            {
                Assert.AreEqual<int>(target.Count, i, string.Format("After adding {0} entries to ArrayQueue, Count returns {1}", i, target.Count));
                target.Enqueue(i);
            }
        }

        /// <summary>
        ///A test for Enqueue
        ///</summary>
        [TestMethod()]
        public void DataOrderPreservedTest()
        {
            ArrayQueue target = new ArrayQueue(); // TODO: Initialize to an appropriate value
            object[] testData = new object[] { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" };
            for (int j = 0; j < 10; j++)
            {
                foreach (var x in testData)
                    target.Enqueue(x);
                foreach (var x in testData)
                    Assert.AreEqual<object>(x, target.Dequeue(), "ArrayQueue dequeueing elements in different order than they're enqueued in");
                Assert.AreEqual<int>(0, target.Count, "ArrayQueue showing wrong count after enqueues and dequeues");
            }
        }

        /// <summary>
        ///A test for Dequeue
        ///</summary>
        [TestMethod()]
        [ExpectedException(typeof(QueueEmptyException))]
        public void DequeueOnEmptyQueueThrowsQueueEmptyExceptionTest()
        {
            ArrayQueue target = new ArrayQueue(); // TODO: Initialize to an appropriate value
            target.Dequeue();
            Assert.Fail("Dequeued from empty queue didn't throw QueueEmptyException");
        }
    }
}
