import { useEffect, useState } from 'react';
import { Trainer } from '../../shared/types';

export const TrainerHome = () => {
  const [trainers, setTrainers] = useState<Trainer[]>([]);

  useEffect(() => {
    fetch('/trainers')
      .then((res) => res.json())
      .then(setTrainers);
  }, []);

  const approve = (id: string) => {
    setTrainers((prev) =>
      prev.map((t) => (t.id === id ? { ...t, status: 'Approved' } : t)),
    );
    fetch(`/trainers/${id}/approve`, { method: 'PUT' });
  };

  return (
    <table>
      <tbody>
        {trainers.map((t) => (
          <tr key={t.id}>
            <td>{t.id}</td>
            <td>{t.name}</td>
            <td>{t.status}</td>
            <td>
              {t.status === 'Pending' && (
                <button onClick={() => approve(t.id)}>Approve</button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
