import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../src/App';

beforeEach(() => {
  global.fetch = jest.fn().mockResolvedValue({
    json: () => Promise.resolve([{ id: 'T-001', name: 'Alice', status: 'Pending' }]),
  }) as any;
});

test('renders trainer row after login', async () => {
  render(<App />);
  screen.getByText('Trainer').click();
  expect(await screen.findByText('Alice')).toBeInTheDocument();
});
