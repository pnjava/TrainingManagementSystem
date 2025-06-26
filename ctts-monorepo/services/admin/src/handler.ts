export const handler = async () => {
  return {
    statusCode: 200,
    body: JSON.stringify({
      totalTrainers: 0,
      pending: 0,
      kitsOrdered: 0,
    }),
  };
};
