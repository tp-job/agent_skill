---
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
tags: [trigger]
---

Is this secure?

```js
app.get('/api/orders/:id', async (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  const user = jwt.decode(token);
  const order = await db.order.findUnique({ where: { id: req.params.id } });
  res.json(order);
});
```
