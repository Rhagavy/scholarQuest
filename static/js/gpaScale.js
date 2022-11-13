//File contains GPA scale used to calculate gpa
const GPA_SCALES = {
  "4.0_12": [
    { letter: "A+", percentage: { min: 90, max: 100 }, gpa: 4 },
    { letter: "A", percentage: { min: 85, max: 89 }, gpa: 3.9 },
    { letter: "A-", percentage: { min: 80, max: 84 }, gpa: 3.7 },
    { letter: "B+", percentage: { min: 77, max: 79 }, gpa: 3.3 },
    { letter: "B", percentage: { min: 73, max: 76 }, gpa: 3 },
    { letter: "B-", percentage: { min: 70, max: 72 }, gpa: 2.7 },
    { letter: "C+", percentage: { min: 67, max: 69 }, gpa: 2.3 },
    { letter: "C", percentage: { min: 63, max: 66 }, gpa: 2 },
    { letter: "C-", percentage: { min: 60, max: 62 }, gpa: 1.7 },
    { letter: "D+", percentage: { min: 57, max: 59 }, gpa: 1.3 },
    { letter: "D", percentage: { min: 53, max: 56 }, gpa: 1 },
    { letter: "D-", percentage: { min: 50, max: 52 }, gpa: 0.7 },
    { letter: "E, F", percentage: { min: 0, max: 49 }, gpa: 0 },
  ],
  "4.0_10": [
    { letter: "A+", percentage: { min: 90, max: 100 }, gpa: 4 },
    { letter: "A", percentage: { min: 85, max: 89 }, gpa: 3.9 },
    { letter: "A-", percentage: { min: 80, max: 84 }, gpa: 3.7 },
    { letter: "B+", percentage: { min: 75, max: 79 }, gpa: 3.3 },
    { letter: "B", percentage: { min: 70, max: 74 }, gpa: 3 },
    { letter: "C+", percentage: { min: 65, max: 69 }, gpa: 2.3 },
    { letter: "C", percentage: { min: 60, max: 64 }, gpa: 2 },
    { letter: "D+", percentage: { min: 55, max: 59 }, gpa: 1.3 },
    { letter: "D", percentage: { min: 50, max: 54 }, gpa: 1 },
    { letter: "E", percentage: { min: 40, max: 49 }, gpa: 0 },
    { letter: "F", percentage: { min: 0, max: 39 }, gpa: 0 },
  ],
  4.3: [
    {
      letter: "A+",
      percentage: {
        min: 90,
        max: 100,
      },
      gpa: 4.3,
    },
    {
      letter: "A",
      percentage: {
        min: 85,
        max: 89.9,
      },
      gpa: 4.0,
    },
    {
      letter: "A-",
      percentage: {
        min: 80,
        max: 84.9,
      },
      gpa: 3.7,
    },
    {
      letter: "B+",
      percentage: {
        min: 77,
        max: 79.9,
      },
      gpa: 3.3,
    },
    {
      letter: "B",
      percentage: {
        min: 73,
        max: 76.9,
      },
      gpa: 3.0,
    },
    {
      letter: "B-",
      percentage: {
        min: 70,
        max: 72.9,
      },
      gpa: 2.7,
    },
    {
      letter: "C+",
      percentage: {
        min: 67,
        max: 69.9,
      },
      gpa: 2.3,
    },
    {
      letter: "C",
      percentage: {
        min: 63,
        max: 66.9,
      },
      gpa: 2.0,
    },
    {
      letter: "C-",
      percentage: {
        min: 60,
        max: 62.9,
      },
      gpa: 1.7,
    },
    {
      letter: "D+",
      percentage: {
        min: 57,
        max: 59.9,
      },
      gpa: 1.3,
    },
    {
      letter: "D",
      percentage: {
        min: 53,
        max: 56.9,
      },
      gpa: 1.0,
    },
    {
      letter: "D-",
      percentage: {
        min: 50,
        max: 52.9,
      },
      gpa: 0.7,
    },
    {
      letter: "F",
      percentage: {
        min: 0,
        max: 49.9,
      },
      gpa: 0.0,
    },
  ],
  4.33: [
    {
      letter: "A+",
      percentage: {
        min: 90,
        max: 100,
      },
      gpa: 4.33,
    },
    {
      letter: "A",
      percentage: {
        min: 85,
        max: 89,
      },
      gpa: 4.0,
    },
    {
      letter: "A-",
      percentage: {
        min: 80,
        max: 84,
      },
      gpa: 3.67,
    },
    {
      letter: "B+",
      percentage: {
        min: 77,
        max: 79,
      },
      gpa: 3.33,
    },
    {
      letter: "B",
      percentage: {
        min: 73,
        max: 76,
      },
      gpa: 3.0,
    },
    {
      letter: "B-",
      percentage: {
        min: 70,
        max: 72,
      },
      gpa: 2.67,
    },
    {
      letter: "C+",
      percentage: {
        min: 67,
        max: 69,
      },
      gpa: 2.33,
    },
    {
      letter: "C",
      percentage: {
        min: 63,
        max: 66,
      },
      gpa: 2.0,
    },
    {
      letter: "C-",
      percentage: {
        min: 60,
        max: 62,
      },
      gpa: 1.67,
    },
    {
      letter: "D+",
      percentage: {
        min: 57,
        max: 59,
      },
      gpa: 1.33,
    },
    {
      letter: "D",
      percentage: {
        min: 53,
        max: 56,
      },
      gpa: 1.0,
    },
    {
      letter: "D-",
      percentage: {
        min: 50,
        max: 52,
      },
      gpa: 0.67,
    },
    {
      letter: "F",
      percentage: {
        min: 0,
        max: 49,
      },
      gpa: 0.0,
    },
  ],
  4.5: [
    {
      letter: "A+",
      percentage: {
        min: 90,
        max: 100,
      },
      gpa: 4.5,
    },
    {
      letter: "A",
      percentage: {
        min: 80,
        max: 89,
      },
      gpa: 4.0,
    },
    {
      letter: "B+",
      percentage: {
        min: 75,
        max: 79,
      },
      gpa: 3.5,
    },
    {
      letter: "B",
      percentage: {
        min: 70,
        max: 74,
      },
      gpa: 3.0,
    },
    {
      letter: "C+",
      percentage: {
        min: 65,
        max: 69,
      },
      gpa: 2.5,
    },
    {
      letter: "C",
      percentage: {
        min: 60,
        max: 64,
      },
      gpa: 2.0,
    },
    {
      letter: "D+",
      percentage: {
        min: 55,
        max: 59,
      },
      gpa: 1.5,
    },
    {
      letter: "D",
      percentage: {
        min: 50,
        max: 54,
      },
      gpa: 1.0,
    },
    {
      letter: "F",
      percentage: {
        min: 0,
        max: 49,
      },
      gpa: 0.0,
    },
  ],
};
