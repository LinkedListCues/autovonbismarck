using EECS214Assignment1;
using Microsoft.VisualStudio.TestTools.UnitTesting;
namespace QueueTests
{
    
    
    /// <summary>
    ///This is a test class for LinkedListQueueTest and is intended
    ///to contain all LinkedListQueueTest Unit Tests
    ///</summary>
    [TestClass()]
    public class LinkedListQueueTest
    {
        [TestMethod()]
        public void LL_ConstructorCreatesEmptyQueueTest()
        {
            LinkedListQueue target = new LinkedListQueue();
            Assert.IsTrue(target.IsEmpty, "A newly created LLQueue should have IsEmpty=true, but doesn't");
        }

        [TestMethod()]
        public void LL_ConstructorCreatesNonFullQueueTest()
        {
            LinkedListQueue target = new LinkedListQueue();
            Assert.IsFalse(target.IsFull, "A newly created LLQueue should have IsFull=false, but doesn't");
        }

        [TestMethod()]
        ///[ExpectedException(typeof(QueueFullException), "Adding to full llqueue should not throw QueueFullException")]
        public void LL_EnqueueToFullQueueThrowsQueueFullExceptionTest()
        {
            LinkedListQueue target = new LinkedListQueue();
            Assert.IsFalse(target.IsFull);
            int i;
            for (i = 0; i < 1000000 && !target.IsFull; i++)
                target.Enqueue(i);
            Assert.IsFalse(target.IsFull, "Added 1000000 elements to LLQueue and it should never fill yp");
            target.Enqueue(0);
            ///Assert.Fail("Enqueue to full queue didn't throw QueueEmptyException");
        }

        /// <summary>
        ///A test for Count
        ///</summary>
        [TestMethod()]
        public void LL_CountTest()
        {
            LinkedListQueue target = new LinkedListQueue();
            for (int i = 0; i < 1000000 && !target.IsFull; i++)
            {
                Assert.AreEqual<int>(target.Count, i, string.Format("After adding {0} entries to LLQueue, Count returns {1}", i, target.Count));
                target.Enqueue(i);
            }
        }

        /// <summary>
        ///A test for Enqueue
        ///</summary>
        [TestMethod()]
        public void LL_DataOrderPreservedTest()
        {
            LinkedListQueue target = new LinkedListQueue(); // TODO: Initialize to an appropriate value
            object[] testData = new object[] { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" };
            for (int j = 0; j < 10; j++)
            {
                foreach (var x in testData)
                    target.Enqueue(x);
                foreach (var x in testData)
                    Assert.AreEqual<object>(x, target.Dequeue(), "LLQueue dequeueing elements in different order than they're enqueued in");
                Assert.AreEqual<int>(0, target.Count, "LLQueue showing wrong count after enqueues and dequeues");
            }
        }

        /// <summary>
        ///A test for Dequeue
        ///</summary>
        [TestMethod()]
        [ExpectedException(typeof(QueueEmptyException))]
        public void LL_DequeueOnEmptyQueueThrowsQueueEmptyExceptionTest()
        {
            LinkedListQueue target = new LinkedListQueue(); // TODO: Initialize to an appropriate value
            target.Dequeue();
            Assert.Fail("Dequeued from empty queue didn't throw QueueEmptyException");
        }
    

    // FILL THIS IN!
}
}
