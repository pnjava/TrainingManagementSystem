import { useEffect, useState } from 'react';

export const AdminHome = () => {
  const [summary, setSummary] = useState<any>(null);
  useEffect(() => {
    fetch('/dashboard/summary')
      .then((res) => res.json())
      .then(setSummary);
  }, []);
  return <pre>{summary ? JSON.stringify(summary, null, 2) : 'Loading...'}</pre>;
};
