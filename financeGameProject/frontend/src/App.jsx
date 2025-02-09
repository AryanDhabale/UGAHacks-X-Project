import React from "react";
import { motion } from "framer-motion";

const FinanceGame = () => {
  return (
    <div className="flex-auto h-screen bg-gray-100 p-60">
      {/* Left Box: User Info */}
      <motion.div
        className="w-2/5 h-3/5 bg-white rounded-2xl shadow-lg p-6 flex flex-col justify-between"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <div className="flex justify-between items-center">
          {/* Placeholder Logo */}
          <div className="w-16 h-16 bg-gray-300 rounded-lg" />
          {/* Account Buttons */}
          <div className="flex space-x-2">
            <button className="w-6 h-6 bg-gray-400 rounded-full" />
            <button className="w-6 h-6 bg-gray-400 rounded-full" />
          </div>
        </div>
        {/* User Info */}
        <div className="text-center mt-6">
          <h2 className="text-2xl font-semibold">User Name</h2>
          <p className="text-gray-500">Level 3 - Junior Analyst</p>
          <div className="w-full bg-gray-200 h-3 rounded-full mt-4">
            <div className="bg-blue-500 h-3 rounded-full" style={{ width: "60%" }} />
          </div>
          <p className="text-sm text-gray-600 mt-2">XP: 1200/2000</p>
        </div>
      </motion.div>
      
      {/* Main Buttons */}
      <div className="flex flex-col justify-center items-center flex-grow space-y-4">
        <button className="px-6 py-3 text-lg bg-blue-600 text-white rounded-xl shadow-md">
          Start Challenge
        </button>
        <button className="px-6 py-3 text-lg bg-green-600 text-white rounded-xl shadow-md">
          View Leaderboard
        </button>
      </div>
    </div>
  );
};

export default FinanceGame;
