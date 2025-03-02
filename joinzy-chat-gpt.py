# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1u3wsETYbb-2knmrIEMQxngpViYgwiNfx
"""

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectItem } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Table } from "@/components/ui/table";
import { Image } from "@/components/ui/image";

export default function JoinzyPlatform() {
  const [activityType, setActivityType] = useState("");
  const activities = ["Football", "Board Game", "Tennis", "Basketball"];

  const parties = [
    {
      partyName: "Weekend Football Match",
      activityType: "Football",
      date: "02/03/2025",
      timeStart: "18:00",
      location: "GameSmith Arena",
      participants: "7/8",
      image: "/football.jpg",
    },
    {
      partyName: "Strategy Board Night",
      activityType: "Board Game",
      date: "03/03/2025",
      timeStart: "19:00",
      location: "GameSmith Cafe",
      participants: "3/4",
      image: "/boardgame.jpg",
    },
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Welcome to Joinzy!</h1>
      <div className="flex gap-4 mb-4">
        <Select value={activityType} onChange={setActivityType} className="w-1/3">
          <SelectItem value="" disabled>Select Activity Type</SelectItem>
          {activities.map((activity) => (
            <SelectItem key={activity} value={activity}>{activity}</SelectItem>
          ))}
        </Select>
        <Button>Create Party</Button>
        <Button>Search Party</Button>
      </div>

      <Table>
        <thead>
          <tr>
            <th>Party Name</th>
            <th>Activity Type</th>
            <th>Date</th>
            <th>Time</th>
            <th>Location</th>
            <th>Participants</th>
            <th>Image</th>
          </tr>
        </thead>
        <tbody>
          {parties.map((party, index) => (
            <tr key={index}>
              <td>{party.partyName}</td>
              <td>{party.activityType}</td>
              <td>{party.date}</td>
              <td>{party.timeStart}</td>
              <td>{party.location}</td>
              <td>{party.participants}</td>
              <td>
                <Image src={party.image} alt={party.partyName} className="w-16 h-16 rounded" />
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}