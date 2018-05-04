using EECS214Assignment1;
using Microsoft.VisualStudio.TestTools.UnitTesting;
namespace QueueTests
{
    
    
    /// <summary>
    ///This is a test class for DequeTest and is intended
    ///to contain all DequeTest Unit Tests
    ///</summary>
    [TestClass()]
    public class DequeTest
    {
        [TestMethod()]
        public void DLL_ConstructorCreatesEmptyQueueTest()
        {
            Deque target = new Deque();
            Assert.IsTrue(target.IsEmpty, "A newly created DLLQueue should have IsEmpty=true, but doesn't");
        }


        /// <summary>
        ///A test for Count
        ///</summary>
        [TestMethod()]
        public void DLL_CountTest()
        {
            Deque target = new Deque();
            for (int i = 0; i < 1000000; i++)
            {
                Assert.AreEqual<int>(target.Count, i, string.Format("After adding {0} entries to LLQueue, Count returns {1}", i, target.Count));
                target.AddEnd(i);
            }
        }

        /// <summary>
        ///A test for Enqueue1
        ///</summary>
        [TestMethod()]
        public void DLL_DataOrderPreservedTest1()
        {
            Deque target = new Deque(); // TODO: Initialize to an appropriate value
            object[] testData = new object[] { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" };
            for (int j = 0; j < 10; j++)
            {
                foreach (var x in testData)
                    target.AddEnd(x);
                foreach (var x in testData)
                    Assert.AreEqual<object>(x, target.RemoveFront(), "DLLQueue dequeueing elements in different order than they're enqueued in");
                Assert.AreEqual<int>(0, target.Count, "DLLQueue showing wrong count after enqueues and dequeues");
            }
        }

        /// <summary>
        ///A test for Enqueue2
        ///</summary>
        [TestMethod()]
        public void DLL_DataOrderPreservedTest2()
        {
            Deque target = new Deque(); // TODO: Initialize to an appropriate value
            object[] testData = new object[] { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" };
            for (int j = 0; j < 10; j++)
            {
                foreach (var x in testData)
                    target.AddFront(x);
                foreach (var x in testData)
                    Assert.AreEqual<object>(x, target.RemoveEnd(), "DLLQueue dequeueing elements in different order than they're enqueued in");
                Assert.AreEqual<int>(0, target.Count, "DLLQueue showing wrong count after enqueues and dequeues");
            }
        }

        /// <summary>
        ///A test for Dequeue2...removeFront when empty
        ///</summary>
        [TestMethod()]
        [ExpectedException(typeof(QueueEmptyException))]
        public void DLL_DequeueOnEmptyQueueThrowsQueueEmptyExceptionTest1()
        {
            Deque target = new Deque(); // TODO: Initialize to an appropriate value
            target.RemoveFront();
            Assert.Fail("Dequeued from empty queue didn't throw QueueEmptyException");
        }

        /// <summary>
        ///A test for Dequeue2...removeEnd when empty
        ///</summary>
        [TestMethod()]
        [ExpectedException(typeof(QueueEmptyException))]
        public void DLL_DequeueOnEmptyQueueThrowsQueueEmptyExceptionTest2()
        {
            Deque target = new Deque(); // TODO: Initialize to an appropriate value
            target.RemoveEnd();
            Assert.Fail("Dequeued from empty queue didn't throw QueueEmptyException");
        }


        // FILL THIS IN!
    }
    // FILL THIS IN!
}

